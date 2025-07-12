from django.db import models
from django.conf import settings
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.User', related_name='projects', 
                              on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Gamification fields
    category = models.ForeignKey('gamification.Category', on_delete=models.CASCADE, 
                                related_name='projects', null=True, blank=True)
    team = models.ForeignKey('gamification.Team', on_delete=models.SET_NULL, 
                            related_name='projects', null=True, blank=True)
    
    # Legacy field - keep for backward compatibility
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                              related_name='project_members',
                                              blank=True)
    
    def __str__(self):
        return self.name
    
    def assign_member(self, user):
        """Assign a user to this project"""
        self.project_members.add(user)
        return True
    
    def get_team_members(self):
        """Get all team members if project is assigned to a team"""
        if self.team:
            return self.team.members.all()
        return self.project_members.all()
    
    class Meta:
        ordering = ['-start_date']


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]


    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    emoji = models.CharField(max_length=10, default='📝')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.SET_NULL, null=True, 
                                    blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                   related_name='created_tasks')
    experience_reward = models.IntegerField(default=10)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def complete_task(self):
        if self.assigned_to and self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.assigned_to.exp_points += self.experience_reward
            self.assigned_to.save()
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-created_at']
