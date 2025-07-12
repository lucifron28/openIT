from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import ActivityLog, UserAchievement, Achievement, GamificationConfig
from .services import GamificationService, WebhookService
from projects.models import Task
from users.models import User


@receiver(post_save, sender=Task)
def handle_task_save(sender, instance, created, **kwargs):
    """Handle task creation and completion"""
    if created:
        # Task created
        GamificationService.log_activity(
            user=instance.created_by,
            action_type='task_created',
            task=instance,
            project=instance.project,
            points_earned=GamificationService.get_points_config('task_created', 25)
        )
    
    elif instance.status == 'completed' and instance.assigned_to:
        # Task completed
        points_earned = GamificationService.get_points_config('task_completed', 100)
        
        # Bonus points for priority
        if instance.priority == 'high':
            points_earned += GamificationService.get_points_config('high_priority_bonus', 50)
        elif instance.priority == 'medium':
            points_earned += GamificationService.get_points_config('medium_priority_bonus', 25)
        
        GamificationService.log_activity(
            user=instance.assigned_to,
            action_type='task_completed',
            task=instance,
            project=instance.project,
            points_earned=points_earned
        )
        
        # Update user points and streak
        GamificationService.update_user_points(instance.assigned_to, points_earned)
        GamificationService.update_user_streak(instance.assigned_to)
        
        # Check for achievements
        GamificationService.check_and_award_achievements(instance.assigned_to)
        
        # Update team challenges
        GamificationService.update_team_challenges(instance)
        
        # Send webhook notifications
        WebhookService.send_task_completion_notification(instance)


@receiver(post_save, sender=UserAchievement)
def handle_achievement_earned(sender, instance, created, **kwargs):
    """Handle achievement earned"""
    if created and instance.progress >= instance.achievement.required_value:
        # Award points for achievement
        GamificationService.update_user_points(
            instance.user, 
            instance.achievement.points_reward
        )
        
        # Log activity
        GamificationService.log_activity(
            user=instance.user,
            action_type='achievement_earned',
            achievement=instance.achievement,
            points_earned=instance.achievement.points_reward
        )
        
        # Send webhook notifications
        WebhookService.send_achievement_notification(instance.user, instance.achievement)


@receiver(post_save, sender=User)
def handle_user_streak_update(sender, instance, **kwargs):
    """Handle streak maintenance"""
    if instance.current_streak > 0:
        # Check for streak achievements
        streak_achievements = Achievement.objects.filter(
            type='streak',
            required_value__lte=instance.current_streak,
            is_active=True
        )
        
        for achievement in streak_achievements:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=instance,
                achievement=achievement,
                defaults={'progress': instance.current_streak}
            )
            
            if not created:
                user_achievement.progress = instance.current_streak
                user_achievement.save()


def initialize_default_achievements():
    """Initialize default achievements"""
    achievements_data = [
        # Task completion achievements
        {
            'name': 'First Steps',
            'description': 'Complete your first task',
            'type': 'task_completion',
            'required_value': 1,
            'points_reward': 100,
            'badge_icon': '🎯',
            'badge_color': '#10B981'
        },
        {
            'name': 'Getting Started',
            'description': 'Complete 10 tasks',
            'type': 'task_completion',
            'required_value': 10,
            'points_reward': 250,
            'badge_icon': '🚀',
            'badge_color': '#3B82F6'
        },
        {
            'name': 'Task Master',
            'description': 'Complete 50 tasks',
            'type': 'task_completion',
            'required_value': 50,
            'points_reward': 500,
            'badge_icon': '👑',
            'badge_color': '#F59E0B'
        },
        {
            'name': 'Legendary Contributor',
            'description': 'Complete 100 tasks',
            'type': 'task_completion',
            'required_value': 100,
            'points_reward': 1000,
            'badge_icon': '🏆',
            'badge_color': '#EF4444'
        },
        
        # Streak achievements
        {
            'name': 'Consistent',
            'description': 'Maintain a 3-day streak',
            'type': 'streak',
            'required_value': 3,
            'points_reward': 150,
            'badge_icon': '🔥',
            'badge_color': '#F97316'
        },
        {
            'name': 'Dedicated',
            'description': 'Maintain a 7-day streak',
            'type': 'streak',
            'required_value': 7,
            'points_reward': 300,
            'badge_icon': '⚡',
            'badge_color': '#8B5CF6'
        },
        {
            'name': 'Unstoppable',
            'description': 'Maintain a 30-day streak',
            'type': 'streak',
            'required_value': 30,
            'points_reward': 1000,
            'badge_icon': '💎',
            'badge_color': '#06B6D4'
        },
        
        # Collaboration achievements
        {
            'name': 'Team Player',
            'description': 'Join your first team',
            'type': 'collaboration',
            'required_value': 1,
            'points_reward': 200,
            'badge_icon': '🤝',
            'badge_color': '#10B981'
        },
        {
            'name': 'Master Collaborator',
            'description': 'Complete 25 assigned tasks',
            'type': 'collaboration',
            'required_value': 25,
            'points_reward': 500,
            'badge_icon': '🌟',
            'badge_color': '#F59E0B'
        },
        
        # Leadership achievements
        {
            'name': 'Leader',
            'description': 'Create your first project',
            'type': 'leadership',
            'required_value': 1,
            'points_reward': 300,
            'badge_icon': '📋',
            'badge_color': '#8B5CF6'
        },
        {
            'name': 'Project Master',
            'description': 'Complete 5 projects',
            'type': 'leadership',
            'required_value': 5,
            'points_reward': 750,
            'badge_icon': '🎖️',
            'badge_color': '#EF4444'
        }
    ]
    
    for achievement_data in achievements_data:
        Achievement.objects.get_or_create(
            name=achievement_data['name'],
            defaults=achievement_data
        )


def initialize_default_config():
    """Initialize default gamification configuration"""
    configs = [
        {
            'name': 'task_created',
            'value': 25,
            'description': 'Points awarded for creating a task'
        },
        {
            'name': 'task_completed',
            'value': 100,
            'description': 'Base points for completing a task'
        },
        {
            'name': 'high_priority_bonus',
            'value': 50,
            'description': 'Bonus points for completing high priority tasks'
        },
        {
            'name': 'medium_priority_bonus',
            'value': 25,
            'description': 'Bonus points for completing medium priority tasks'
        },
        {
            'name': 'team_joined',
            'value': 50,
            'description': 'Points for joining a team'
        },
        {
            'name': 'project_created',
            'value': 200,
            'description': 'Points for creating a project'
        },
        {
            'name': 'streak_multiplier',
            'value': 1.5,
            'description': 'Multiplier for maintaining streaks'
        }
    ]
    
    for config in configs:
        GamificationConfig.objects.get_or_create(
            name=config['name'],
            defaults=config
        )
