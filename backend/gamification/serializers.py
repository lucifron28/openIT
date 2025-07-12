from rest_framework import serializers
from .models import (
    Category, Team, TeamMembership, Achievement, UserAchievement,
    TeamChallenge, GamificationConfig, WebhookConfig, ActivityLog
)
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    team_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', 'description', 'icon', 'color', 'team_count']
    
    def get_team_count(self, obj):
        return obj.teams.filter(is_active=True).count()


class TeamMembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    points = serializers.IntegerField(source='user.points', read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = ['user', 'username', 'email', 'avatar', 'points', 'role', 'joined_at', 'points_contributed']


class TeamSerializer(serializers.ModelSerializer):
    administrator_username = serializers.CharField(source='administrator.username', read_only=True)
    category_name = serializers.CharField(source='category.display_name', read_only=True)
    member_count = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    members = TeamMembershipSerializer(source='teammembership_set', many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'administrator', 'administrator_username', 'avatar', 'is_active',
            'max_members', 'is_public', 'member_count', 'total_points',
            'members', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.get_member_count()
    
    def get_total_points(self, obj):
        return obj.get_total_points()
    
    def create(self, validated_data):
        validated_data['administrator'] = self.context['request'].user
        return super().create(validated_data)


class AchievementSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.display_name', read_only=True)
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'type', 'category', 'category_name',
            'required_value', 'points_reward', 'badge_icon', 'badge_color',
            'is_active', 'is_hidden'
        ]


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAchievement
        fields = ['achievement', 'earned_at', 'progress', 'progress_percentage']
    
    def get_progress_percentage(self, obj):
        if obj.achievement.required_value == 0:
            return 100
        return min(100, (obj.progress / obj.achievement.required_value) * 100)


class TeamChallengeSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamChallenge
        fields = [
            'id', 'name', 'description', 'team', 'team_name',
            'target_type', 'target_value', 'current_progress', 'progress_percentage',
            'start_date', 'end_date', 'status', 'is_active',
            'points_reward', 'badge_reward', 'created_by', 'created_by_username'
        ]
        read_only_fields = ['id', 'current_progress', 'created_by']
    
    def get_progress_percentage(self, obj):
        return obj.progress_percentage()
    
    def get_is_active(self, obj):
        return obj.is_active()
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ActivityLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    task_name = serializers.CharField(source='task.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'username', 'action_type', 'points_earned',
            'task', 'task_name', 'project', 'project_name',
            'team', 'team_name', 'achievement', 'achievement_name',
            'metadata', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.CharField()
    points = serializers.IntegerField()
    achievements_count = serializers.IntegerField()
    tasks_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    rank = serializers.IntegerField()


class TeamLeaderboardSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    team_name = serializers.CharField()
    avatar = serializers.CharField()
    total_points = serializers.IntegerField()
    member_count = serializers.IntegerField()
    completed_challenges = serializers.IntegerField()
    rank = serializers.IntegerField()


class GamificationStatsSerializer(serializers.Serializer):
    total_points = serializers.IntegerField()
    achievements_earned = serializers.IntegerField()
    tasks_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    teams_joined = serializers.IntegerField()
    rank_position = serializers.IntegerField()
    recent_achievements = UserAchievementSerializer(many=True)
    recent_activities = ActivityLogSerializer(many=True)
