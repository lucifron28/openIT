from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction, models
from django.utils import timezone
from django.db.models import Count, Sum, Q
from .models import (
    Category, Team, TeamMembership, Achievement, UserAchievement,
    TeamChallenge, ActivityLog
)
from .serializers import (
    CategorySerializer, TeamSerializer, TeamMembershipSerializer,
    AchievementSerializer, UserAchievementSerializer, TeamChallengeSerializer,
    ActivityLogSerializer, LeaderboardSerializer, TeamLeaderboardSerializer,
    GamificationStatsSerializer
)
from .services import GamificationService, WebhookService
from users.models import User


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            # Show teams user is member of or public teams
            return Team.objects.filter(
                Q(members=user) | Q(is_public=True)
            ).distinct().select_related('category', 'administrator')
        return Team.objects.all()
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        user = request.user
        
        if team.members.filter(id=user.id).exists():
            return Response({'error': 'Already a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not team.is_public:
            return Response({'error': 'This team is private'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        if team.get_member_count() >= team.max_members:
            return Response({'error': 'Team is full'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        TeamMembership.objects.create(user=user, team=team, role='member')
        
        # Log activity
        GamificationService.log_activity(
            user=user,
            action_type='team_joined',
            team=team,
            points_earned=50
        )
        
        # Send webhook notification
        WebhookService.send_team_join_notification(team, user)
        
        return Response({'message': f'Successfully joined {team.name}'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        user = request.user
        
        if team.administrator == user:
            return Response({'error': 'Team administrator cannot leave. Transfer ownership first.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        membership = TeamMembership.objects.filter(user=user, team=team).first()
        if not membership:
            return Response({'error': 'Not a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        membership.delete()
        return Response({'message': f'Successfully left {team.name}'})
    
    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get team leaderboard"""
        team = self.get_object()
        
        # Check if user is member
        if not team.members.filter(id=request.user.id).exists():
            return Response({'error': 'Access denied'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        members = User.objects.filter(teams=team).annotate(
            achievements_count=Count('achievements'),
            tasks_completed=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed'))
        ).order_by('-points')
        
        leaderboard_data = []
        for rank, member in enumerate(members, 1):
            leaderboard_data.append({
                'user_id': member.id,
                'username': member.username,
                'avatar': member.avatar,
                'points': member.points,
                'achievements_count': member.achievements_count,
                'tasks_completed': member.tasks_completed,
                'current_streak': member.current_streak,
                'rank': rank
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def challenges(self, request, pk=None):
        """Get team challenges"""
        team = self.get_object()
        challenges = team.challenges.all().order_by('-created_at')
        serializer = TeamChallengeSerializer(challenges, many=True)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Achievement.objects.filter(is_active=True)
        
        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        
        # Filter by type if provided
        achievement_type = self.request.query_params.get('type')
        if achievement_type:
            queryset = queryset.filter(type=achievement_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get user's earned achievements"""
        user_achievements = UserAchievement.objects.filter(
            user=request.user
        ).select_related('achievement')
        
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """Get achievement progress for all achievements"""
        achievements = Achievement.objects.filter(is_active=True)
        progress_data = []
        
        for achievement in achievements:
            user_achievement = UserAchievement.objects.filter(
                user=request.user, achievement=achievement
            ).first()
            
            if user_achievement:
                progress = user_achievement.progress
                earned = user_achievement.earned_at is not None
            else:
                progress = GamificationService.calculate_achievement_progress(
                    request.user, achievement
                )
                earned = False
            
            progress_data.append({
                'achievement': AchievementSerializer(achievement).data,
                'progress': progress,
                'earned': earned,
                'progress_percentage': min(100, (progress / achievement.required_value) * 100)
            })
        
        return Response(progress_data)


class TeamChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = TeamChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show challenges for teams user is member of
        user_teams = self.request.user.teams.all()
        return TeamChallenge.objects.filter(team__in=user_teams)
    
    def perform_create(self, serializer):
        team = serializer.validated_data['team']
        
        # Check if user is admin or moderator of the team
        membership = TeamMembership.objects.filter(
            user=self.request.user, 
            team=team, 
            role__in=['admin', 'moderator']
        ).first()
        
        if not membership and team.administrator != self.request.user:
            raise PermissionError("Only team administrators and moderators can create challenges")
        
        serializer.save(created_by=self.request.user)


class LeaderboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def global_leaderboard(self, request):
        """Global user leaderboard"""
        users = User.objects.annotate(
            achievements_count=Count('achievements'),
            tasks_completed=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed'))
        ).order_by('-points')[:50]  # Top 50
        
        leaderboard_data = []
        for rank, user in enumerate(users, 1):
            leaderboard_data.append({
                'user_id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'points': user.points,
                'achievements_count': user.achievements_count,
                'tasks_completed': user.tasks_completed,
                'current_streak': user.current_streak,
                'rank': rank
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def team_leaderboard(self, request):
        """Team leaderboard"""
        teams = Team.objects.filter(is_active=True).annotate(
            total_points=Sum('members__points'),
            member_count=Count('members'),
            completed_challenges=Count('challenges', filter=Q(challenges__status='completed'))
        ).order_by('-total_points')[:20]  # Top 20 teams
        
        leaderboard_data = []
        for rank, team in enumerate(teams, 1):
            leaderboard_data.append({
                'team_id': team.id,
                'team_name': team.name,
                'avatar': team.avatar,
                'total_points': team.total_points or 0,
                'member_count': team.member_count,
                'completed_challenges': team.completed_challenges,
                'rank': rank
            })
        
        serializer = TeamLeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get comprehensive user statistics"""
        user = request.user
        
        # Recent achievements (last 5)
        recent_achievements = UserAchievement.objects.filter(
            user=user
        ).select_related('achievement').order_by('-earned_at')[:5]
        
        # Recent activities (last 10)
        recent_activities = ActivityLog.objects.filter(
            user=user
        ).select_related('task', 'project', 'team', 'achievement').order_by('-timestamp')[:10]
        
        # User rank
        user_rank = User.objects.filter(points__gt=user.points).count() + 1
        
        stats_data = {
            'total_points': user.points,
            'achievements_earned': user.achievements.count(),
            'tasks_completed': user.assigned_tasks.filter(status='completed').count(),
            'current_streak': user.current_streak,
            'longest_streak': user.longest_streak,
            'teams_joined': user.teams.count(),
            'rank_position': user_rank,
            'recent_achievements': UserAchievementSerializer(recent_achievements, many=True).data,
            'recent_activities': ActivityLogSerializer(recent_activities, many=True).data
        }
        
        serializer = GamificationStatsSerializer(stats_data)
        return Response(serializer.data)


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ActivityLog.objects.filter(user=self.request.user)
        
        # Filter by action type if provided
        action_type = self.request.query_params.get('action_type')
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset.select_related('task', 'project', 'team', 'achievement')
