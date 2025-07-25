# Generated by Django 5.2.4 on 2025-07-12 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_project_project_members'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('classroom', 'Classroom Team'), ('software', 'Software Development Team'), ('sales', 'Sales Team')], max_length=50, unique=True)),
                ('display_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(default='📚', max_length=50)),
                ('color', models.CharField(default='#3B82F6', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='GamificationConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', models.JSONField()),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Gamification Configuration',
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('task_completion', 'Task Completion'), ('streak', 'Streak'), ('collaboration', 'Collaboration'), ('leadership', 'Leadership'), ('category_specific', 'Category Specific'), ('team_challenge', 'Team Challenge')], max_length=20)),
                ('required_value', models.IntegerField(help_text='Required value to unlock (e.g., 10 tasks, 7 day streak)')),
                ('points_reward', models.IntegerField(default=100)),
                ('badge_icon', models.CharField(default='🏆', max_length=10)),
                ('badge_color', models.CharField(default='#FFD700', max_length=7)),
                ('is_active', models.BooleanField(default=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.category')),
            ],
            options={
                'ordering': ['type', 'required_value'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('avatar', models.CharField(default='👥', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_members', models.IntegerField(default=50)),
                ('is_public', models.BooleanField(default=True)),
                ('administrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administered_teams', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='gamification.category')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('task_created', 'Task Created'), ('task_completed', 'Task Completed'), ('task_assigned', 'Task Assigned'), ('project_created', 'Project Created'), ('team_joined', 'Team Joined'), ('achievement_earned', 'Achievement Earned'), ('streak_maintained', 'Streak Maintained')], max_length=20)),
                ('points_earned', models.IntegerField(default=0)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.achievement')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.team')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='TeamChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('target_type', models.CharField(choices=[('tasks_completed', 'Tasks Completed'), ('projects_finished', 'Projects Finished'), ('points_earned', 'Points Earned'), ('collaboration_score', 'Collaboration Score')], max_length=50)),
                ('target_value', models.IntegerField()),
                ('current_progress', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='upcoming', max_length=20)),
                ('points_reward', models.IntegerField(default=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('badge_reward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gamification.achievement')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='gamification.team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator'), ('admin', 'Administrator')], default='member', max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('points_contributed', models.IntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'team')},
            },
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='teams', through='gamification.TeamMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WebhookConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('platform', models.CharField(choices=[('discord', 'Discord'), ('teams', 'Microsoft Teams')], max_length=20)),
                ('webhook_url', models.URLField()),
                ('notify_task_completion', models.BooleanField(default=True)),
                ('notify_achievements', models.BooleanField(default=True)),
                ('notify_team_challenges', models.BooleanField(default=True)),
                ('notify_milestones', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webhooks', to='gamification.team')),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('progress', models.IntegerField(default=0)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamification.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-earned_at'],
                'unique_together': {('user', 'achievement')},
            },
        ),
    ]
