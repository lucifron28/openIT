from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.User', related_name='projects', on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)