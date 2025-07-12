import requests
import json
from django.utils import timezone
from django.db.models import Count, Q
from .models import (
    ActivityLog, UserAchievement, Achievement, GamificationConfig,
    WebhookConfig, TeamChallenge
)
from users.models import User


class GamificationService:
    """Service for handling gamification logic"""
    
    @staticmethod
    def log_activity(user, action_type, points_earned=0, **kwargs):
        """Log user activity"""
        return ActivityLog.objects.create(
            user=user,
            action_type=action_type,
            points_earned=points_earned,
            task=kwargs.get('task'),
            project=kwargs.get('project'),
            team=kwargs.get('team'),
            achievement=kwargs.get('achievement'),
            metadata=kwargs.get('metadata', {})
        )
    
    @staticmethod
    def update_user_points(user, points):
        user.points += points
        user.save(update_fields=['points'])
    
    @staticmethod
    def award_points(user, action_type, points):
        """Award points to user and log activity"""
        GamificationService.update_user_points(user, points)
        
        GamificationService.log_activity(
            user=user,
            action_type=action_type,
            points_earned=points
        )
        
        GamificationService.update_user_streak(user)
        
        # Check for achievements
        GamificationService.check_and_award_achievements(user)
        
        return True
    
    @staticmethod
    def check_achievements(user):
        """Check and return unlocked achievements for user"""
        GamificationService.check_and_award_achievements(user)
        
        # Return recently earned achievements
        recent_achievements = UserAchievement.objects.filter(
            user=user,
            earned_at__isnull=False
        ).select_related('achievement').order_by('-earned_at')
        
        return [ua.achievement for ua in recent_achievements]
    
    @staticmethod
    def update_user_streak(user):
        """Update user streak based on recent activity"""
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        # Check if user has activity today
        has_activity_today = ActivityLog.objects.filter(
            user=user,
            timestamp__date=today,
            action_type='task_completed'
        ).exists()
        
        # Check if user had activity yesterday
        has_activity_yesterday = ActivityLog.objects.filter(
            user=user,
            timestamp__date=yesterday,
            action_type='task_completed'
        ).exists()
        
        if has_activity_today:
            if has_activity_yesterday or user.current_streak == 0:
                user.current_streak += 1
            user.last_activity_date = today
            
            # Update longest streak
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
                
        elif not has_activity_yesterday and user.current_streak > 0:
            # Streak broken
            user.current_streak = 0
        
        user.save(update_fields=['current_streak', 'longest_streak', 'last_activity_date'])
    
    @staticmethod
    def check_and_award_achievements(user):
        """Check and award achievements for user"""
        # Task completion achievements
        tasks_completed = user.assigned_tasks.filter(status='completed').count()
        task_achievements = Achievement.objects.filter(
            type='task_completion',
            required_value__lte=tasks_completed,
            is_active=True
        )
        
        for achievement in task_achievements:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'progress': tasks_completed}
            )
            
            if not created:
                user_achievement.progress = tasks_completed
                user_achievement.save()
        
        # Collaboration achievements
        assigned_tasks_completed = user.assigned_tasks.filter(
            status='completed'
        ).exclude(created_by=user).count()
        
        collab_achievements = Achievement.objects.filter(
            type='collaboration',
            required_value__lte=assigned_tasks_completed,
            is_active=True
        )
        
        for achievement in collab_achievements:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'progress': assigned_tasks_completed}
            )
            
            if not created:
                user_achievement.progress = assigned_tasks_completed
                user_achievement.save()
        
        # Leadership achievements
        projects_created = user.projects.count()
        leadership_achievements = Achievement.objects.filter(
            type='leadership',
            required_value__lte=projects_created,
            is_active=True
        )
        
        for achievement in leadership_achievements:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement,
                defaults={'progress': projects_created}
            )
            
            if not created:
                user_achievement.progress = projects_created
                user_achievement.save()
    
    @staticmethod
    def calculate_achievement_progress(user, achievement):
        """Calculate current progress for an achievement"""
        if achievement.type == 'task_completion':
            return user.assigned_tasks.filter(status='completed').count()
        elif achievement.type == 'streak':
            return user.current_streak
        elif achievement.type == 'collaboration':
            return user.assigned_tasks.filter(
                status='completed'
            ).exclude(created_by=user).count()
        elif achievement.type == 'leadership':
            return user.projects.count()
        else:
            return 0
    
    @staticmethod
    def update_team_challenges(task):
        """Update team challenge progress when tasks are completed"""
        if not task.assigned_to:
            return
        
        user_teams = task.assigned_to.teams.all()
        active_challenges = TeamChallenge.objects.filter(
            team__in=user_teams,
            status='active',
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        
        for challenge in active_challenges:
            if challenge.target_type == 'tasks_completed':
                challenge.current_progress += 1
                challenge.save(update_fields=['current_progress'])
                
                # Check if challenge is completed
                if challenge.current_progress >= challenge.target_value:
                    challenge.status = 'completed'
                    challenge.save(update_fields=['status'])
                    
                    # Award points to all team members
                    for member in challenge.team.members.all():
                        GamificationService.update_user_points(
                            member, 
                            challenge.points_reward
                        )
    
    @staticmethod
    def get_points_config(config_name, default_value):
        """Get points configuration value"""
        try:
            config = GamificationConfig.objects.get(name=config_name, is_active=True)
            return config.value
        except GamificationConfig.DoesNotExist:
            return default_value


class WebhookService:
    """Service for handling webhook notifications"""
    
    @staticmethod
    def send_webhook_notification(webhook_config, payload):
        """Send webhook notification"""
        try:
            if webhook_config.platform == 'discord':
                return WebhookService._send_discord_webhook(webhook_config.webhook_url, payload)
            elif webhook_config.platform == 'teams':
                return WebhookService._send_teams_webhook(webhook_config.webhook_url, payload)
        except Exception as e:
            print(f"Webhook error: {e}")
            return False
    
    @staticmethod
    def _send_discord_webhook(webhook_url, payload):
        """Send Discord webhook"""
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 204
    
    @staticmethod
    def _send_teams_webhook(webhook_url, payload):
        """Send Microsoft Teams webhook"""
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    
    @staticmethod
    def send_task_completion_notification(task):
        """Send task completion notification"""
        if not task.assigned_to:
            return
        
        user_teams = task.assigned_to.teams.all()
        webhook_configs = WebhookConfig.objects.filter(
            team__in=user_teams,
            notify_task_completion=True,
            is_active=True
        )
        
        for config in webhook_configs:
            if config.platform == 'discord':
                payload = {
                    "embeds": [{
                        "title": "Task Completed! 🎉",
                        "description": f"**{task.assigned_to.username}** completed task: **{task.name}**",
                        "color": 5763719,  # Green color
                        "fields": [
                            {
                                "name": "Project",
                                "value": task.project.name,
                                "inline": True
                            },
                            {
                                "name": "Priority",
                                "value": task.priority.title(),
                                "inline": True
                            },
                            {
                                "name": "Points Earned",
                                "value": f"+{task.experience_reward}",
                                "inline": True
                            }
                        ],
                        "timestamp": timezone.now().isoformat()
                    }]
                }
            else:  # Teams
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "themeColor": "00FF00",
                    "summary": "Task Completed",
                    "sections": [{
                        "activityTitle": "Task Completed! 🎉",
                        "activitySubtitle": f"{task.assigned_to.username} completed a task",
                        "facts": [
                            {"name": "Task", "value": task.name},
                            {"name": "Project", "value": task.project.name},
                            {"name": "Priority", "value": task.priority.title()},
                            {"name": "Points", "value": f"+{task.experience_reward}"}
                        ]
                    }]
                }
            
            WebhookService.send_webhook_notification(config, payload)
    
    @staticmethod
    def send_achievement_notification(user, achievement):
        """Send achievement earned notification"""
        user_teams = user.teams.all()
        webhook_configs = WebhookConfig.objects.filter(
            team__in=user_teams,
            notify_achievements=True,
            is_active=True
        )
        
        for config in webhook_configs:
            if config.platform == 'discord':
                payload = {
                    "embeds": [{
                        "title": f"Achievement Unlocked! {achievement.badge_icon}",
                        "description": f"**{user.username}** earned: **{achievement.name}**",
                        "color": int(achievement.badge_color.replace('#', ''), 16),
                        "fields": [
                            {
                                "name": "Description",
                                "value": achievement.description,
                                "inline": False
                            },
                            {
                                "name": "Points Reward",
                                "value": f"+{achievement.points_reward}",
                                "inline": True
                            }
                        ],
                        "timestamp": timezone.now().isoformat()
                    }]
                }
            else:  # Teams
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "themeColor": achievement.badge_color.replace('#', ''),
                    "summary": "Achievement Unlocked",
                    "sections": [{
                        "activityTitle": f"Achievement Unlocked! {achievement.badge_icon}",
                        "activitySubtitle": f"{user.username} earned a new achievement",
                        "facts": [
                            {"name": "Achievement", "value": achievement.name},
                            {"name": "Description", "value": achievement.description},
                            {"name": "Points", "value": f"+{achievement.points_reward}"}
                        ]
                    }]
                }
            
            WebhookService.send_webhook_notification(config, payload)
    
    @staticmethod
    def send_team_join_notification(team, user):
        """Send team join notification"""
        webhook_configs = WebhookConfig.objects.filter(
            team=team,
            is_active=True
        )
        
        for config in webhook_configs:
            if config.platform == 'discord':
                payload = {
                    "embeds": [{
                        "title": "New Team Member! 👋",
                        "description": f"**{user.username}** joined the team **{team.name}**",
                        "color": 3447003,  # Blue color
                        "timestamp": timezone.now().isoformat()
                    }]
                }
            else:  # Teams
                payload = {
                    "@type": "MessageCard",
                    "@context": "http://schema.org/extensions",
                    "themeColor": "0076D7",
                    "summary": "New Team Member",
                    "sections": [{
                        "activityTitle": "New Team Member! 👋",
                        "activitySubtitle": f"{user.username} joined {team.name}"
                    }]
                }
            
            WebhookService.send_webhook_notification(config, payload)
