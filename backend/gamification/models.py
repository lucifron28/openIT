from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User

# NOTE: Achievement categories
class Category(models.Model):
    CATEGORY_CHOICES = [
        ('classroom', 'Classroom Team'),
        ('software', 'Software Development Team'),
        ('sales', 'Sales Team'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='📚')  # Emoji or icon class
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name_plural = "Categories"


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='teams')
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_teams')
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')
    avatar = models.CharField(max_length=10, default='👥')  # Team emoji
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Team settings
    max_members = models.IntegerField(default=50)
    is_public = models.BooleanField(default=True)  # Can users join freely
    
    def __str__(self):
        return self.name
    
    def get_member_count(self):
        return self.members.count()
    
    def get_total_points(self):
        return sum(member.points for member in self.members.all())
    
    class Meta:
        ordering = ['-created_at']


class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    points_contributed = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'team']


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('task_completion', 'Task Completion'),
        ('streak', 'Streak'),
        ('collaboration', 'Collaboration'),
        ('leadership', 'Leadership'),
        ('category_specific', 'Category Specific'),
        ('team_challenge', 'Team Challenge'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    # Achievement criteria
    required_value = models.IntegerField(help_text="Required value to unlock (e.g., 10 tasks, 7 day streak)")
    points_reward = models.IntegerField(default=100)
    
    # Badge design
    badge_icon = models.CharField(max_length=10, default='🏆')
    badge_color = models.CharField(max_length=7, default='#FFD700')
    
    # Rarity and visibility
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)  # Hidden until unlocked
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['type', 'required_value']


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # Current progress towards achievement
    
    class Meta:
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']


class TeamChallenge(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='challenges')
    
    # Challenge criteria
    target_type = models.CharField(max_length=50, choices=[
        ('tasks_completed', 'Tasks Completed'),
        ('projects_finished', 'Projects Finished'),
        ('points_earned', 'Points Earned'),
        ('collaboration_score', 'Collaboration Score'),
    ])
    target_value = models.IntegerField()
    current_progress = models.IntegerField(default=0)
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    
    # Rewards
    points_reward = models.IntegerField(default=500)
    badge_reward = models.ForeignKey(Achievement, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.team.name} - {self.name}"
    
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.status == 'active'
    
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_progress / self.target_value) * 100)


class GamificationConfig(models.Model):
    """Configuration for gamification rules and point values"""
    name = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Gamification Configuration"


class WebhookConfig(models.Model):
    PLATFORM_CHOICES = [
        ('discord', 'Discord'),
        ('teams', 'Microsoft Teams'),
    ]
    
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    webhook_url = models.URLField(max_length=500)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='webhooks', null=True, blank=True)
    
    # Event triggers
    notify_task_completion = models.BooleanField(default=True)
    notify_achievements = models.BooleanField(default=True)
    notify_team_challenges = models.BooleanField(default=True)
    notify_milestones = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.platform})"


class ActivityLog(models.Model):
    """Log of user activities for points calculation and analytics"""
    ACTION_TYPES = [
        ('task_created', 'Task Created'),
        ('task_completed', 'Task Completed'),
        ('task_assigned', 'Task Assigned'),
        ('project_created', 'Project Created'),
        ('team_joined', 'Team Joined'),
        ('achievement_earned', 'Achievement Earned'),
        ('streak_maintained', 'Streak Maintained'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    points_earned = models.IntegerField(default=0)
    
    # Related objects
    task = models.ForeignKey('projects.Task', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=True, blank=True)
    
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.action_type} (+{self.points_earned} points)"
    
    class Meta:
        ordering = ['-timestamp']
