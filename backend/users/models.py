from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Gamification fields
    points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Profile fields
    avatar = models.CharField(max_length=10, default='👤')  # Emoji avatar
    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.username
    
    def get_rank(self):
        """Get user's rank based on points"""
        return User.objects.filter(points__gt=self.points).count() + 1
    
    def get_total_achievements(self):
        """Get total number of achievements earned"""
        return self.achievements.count()
    
    def get_completed_tasks(self):
        """Get total number of completed tasks"""
        return self.assigned_tasks.filter(status='completed').count()