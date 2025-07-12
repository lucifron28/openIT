from rest_framework import serializers
from .models import Project, Task
from users.models import User


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.EmailField(read_only=True)
    assigned_to_username = serializers.CharField(read_only=True)
    created_by_username = serializers.CharField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'assigned_to_email', 'assigned_to_username',
            'created_by', 'created_by_username', 'experience_reward',
            'due_date', 'completed_at', 'created_at', 'updated_at', 'project'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_task_count = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.display_name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    project_members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date', 'updated_at',
            'owner', 'owner_username', 'emoji', 'is_active', 'category', 'category_name',
            'team', 'team_name', 'tasks', 'task_count', 'completed_task_count', 'project_members'
        ]
        read_only_fields = ['id', 'start_date', 'updated_at']

    # NOTE: Assigns a user to the Project
    def assign_member(self, user):
        if user not in self.project_members.all():
            self.project_members.add(user)
            self.save()
        return user

    def get_task_count(self, obj):
        return obj.tasks.count()


    def get_completed_task_count(self, obj):
        return obj.tasks.filter(status='completed').count()

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'experience_reward', 'due_date', 'project'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'experience_reward', 'due_date'
        ]