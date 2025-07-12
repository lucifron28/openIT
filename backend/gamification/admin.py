from django.contrib import admin
from .models import (
    Category, Team, TeamMembership, Achievement, UserAchievement,
    TeamChallenge, GamificationConfig, WebhookConfig, ActivityLog
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'icon', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'display_name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'administrator', 'is_active', 'member_count', 'created_at']
    list_filter = ['category', 'is_active', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'administrator__username']
    
    def member_count(self, obj):
        return obj.get_member_count()
    member_count.short_description = 'Members'


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'role', 'points_contributed', 'joined_at']
    list_filter = ['role', 'joined_at', 'team__category']
    search_fields = ['user__username', 'team__name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'category', 'required_value', 'points_reward', 'badge_icon', 'is_active']
    list_filter = ['type', 'category', 'is_active', 'is_hidden']
    search_fields = ['name', 'description']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'type', 'category')
        }),
        ('Criteria', {
            'fields': ('required_value', 'points_reward')
        }),
        ('Badge Design', {
            'fields': ('badge_icon', 'badge_color')
        }),
        ('Visibility', {
            'fields': ('is_active', 'is_hidden')
        }),
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'progress', 'earned_at']
    list_filter = ['achievement__type', 'earned_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['earned_at']


@admin.register(TeamChallenge)
class TeamChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'target_type', 'progress_display', 'status', 'start_date', 'end_date']
    list_filter = ['status', 'target_type', 'start_date', 'team__category']
    search_fields = ['name', 'team__name']
    readonly_fields = ['current_progress']
    
    def progress_display(self, obj):
        return f"{obj.current_progress}/{obj.target_value} ({obj.progress_percentage():.1f}%)"
    progress_display.short_description = 'Progress'


@admin.register(GamificationConfig)
class GamificationConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['name', 'description']


@admin.register(WebhookConfig)
class WebhookConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'team', 'is_active', 'created_at']
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['name', 'team__name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'platform', 'webhook_url', 'team')
        }),
        ('Notification Settings', {
            'fields': ('notify_task_completion', 'notify_achievements', 
                      'notify_team_challenges', 'notify_milestones')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'points_earned', 'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['user__username', 'action_type']
    readonly_fields = ['timestamp']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'task', 'project', 'team', 'achievement'
        )
