from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    team_id = models.IntegerField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

