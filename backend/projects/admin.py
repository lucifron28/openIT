from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'start_date', 'updated_at']
    list_filter = ['is_active', 'start_date', 'owner']
    search_fields = ['name', 'description', 'owner__username']
    readonly_fields = ['start_date', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'project', 'status', 'priority', 'assigned_to', 
        'created_by', 'due_date', 'created_at'
    ]
    list_filter = ['status', 'priority', 'project', 'created_at']
    search_fields = [
        'name', 'description', 'project__name', 
        'assigned_to__username', 'created_by__username'
    ]
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'emoji', 'project')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by', 'status', 'priority')
        }),
        ('Rewards & Timing', {
            'fields': ('experience_reward', 'due_date', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'project', 'assigned_to', 'created_by'
        )
