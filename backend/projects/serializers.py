from rest_framework import serializers
from .models import Project, Task
from users.models import User

class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'avatar']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_email = serializers.SerializerMethodField()
    assigned_to_username = serializers.SerializerMethodField()
    created_by_username = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'assigned_to_email', 'assigned_to_username',
            'created_by', 'created_by_username', 'experience_reward',
            'due_date', 'completed_at', 'created_at', 'updated_at', 'project'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def get_assigned_to_email(self, obj):
        return obj.assigned_to.email if obj.assigned_to else None
    def get_assigned_to_username(self, obj):
        return obj.assigned_to.username if obj.assigned_to else None
    def get_created_by_username(self, obj):
        return obj.created_by.username if obj.created_by else None

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    project_members = UserLiteSerializer(many=True, read_only=True)
    project_members_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'emoji', 'owner', 'owner_username',
            'tasks', 'project_members', 'project_members_ids'
        ]
        read_only_fields = ['id', 'owner', 'tasks', 'project_members', 'owner_username']

    def create(self, validated_data):
        members = validated_data.pop('project_members_ids', [])
        validated_data['owner'] = self.context['request'].user
        project = super().create(validated_data)
        if members:
            project.project_members.set(members)
        return project

    def update(self, instance, validated_data):
        members = validated_data.pop('project_members_ids', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.project_members.set(members)
        return instance

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'experience_reward', 'due_date', 'project'
        ]

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name', 'description', 'status', 'priority', 'emoji',
            'assigned_to', 'experience_reward', 'due_date'
        ]
