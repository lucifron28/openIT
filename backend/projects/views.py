from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction, models
from django.utils import timezone
from .models import Project, Task
from .serializers import (
    ProjectSerializer, TaskSerializer, 
    TaskCreateSerializer, TaskUpdateSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user).prefetch_related('tasks')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get all tasks for a specific project"""
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_task(self, request, pk=None):
        """Create a new task for this project"""
        project = self.get_object()
        serializer = TaskCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get project statistics"""
        project = self.get_object()
        tasks = project.tasks.all()
        
        stats = {
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(status='completed').count(),
            'in_progress_tasks': tasks.filter(status='in_progress').count(),
            'todo_tasks': tasks.filter(status='todo').count(),
            'high_priority_tasks': tasks.filter(priority='high').count(),
            'overdue_tasks': tasks.filter(
                due_date__lt=timezone.now(),
                status__in=['todo', 'in_progress']
            ).count() if hasattr(tasks.first(), 'due_date') else 0,
        }
        
        return Response(stats)

    @action(detail=True, methods=['post'])
    def assign_member(self, request, pk=None):
        """Assign a user to the project"""
        project = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            project.assign_member(user)
            return Response({'message': f'User {user.username} assigned to project {project.name}'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can see tasks they created or are assigned to
        return Task.objects.filter(
            models.Q(created_by=self.request.user) | 
            models.Q(assigned_to=self.request.user) |
            models.Q(project__owner=self.request.user)
        ).select_related('project', 'assigned_to', 'created_by')

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed and award experience"""
        task = self.get_object()
        
        # Check if user has permission to complete this task
        if task.assigned_to != request.user and task.created_by != request.user:
            return Response(
                {'error': 'You do not have permission to complete this task'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        with transaction.atomic():
            if task.complete_task():
                serializer = self.get_serializer(task)
                return Response({
                    'message': 'Task completed successfully',
                    'experience_gained': task.experience_reward,
                    'task': serializer.data
                })
            else:
                return Response(
                    {'error': 'Task could not be completed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """Get tasks assigned to the current user"""
        tasks = self.get_queryset().filter(assigned_to=request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        
        # Filter by priority if provided
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
        
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def created_by_me(self, request):
        """Get tasks created by the current user"""
        tasks = self.get_queryset().filter(created_by=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign task to a user"""
        task = self.get_object()
        
        # Only task creator or project owner can assign tasks
        if task.created_by != request.user and task.project.owner != request.user:
            return Response(
                {'error': 'You do not have permission to assign this task'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            task.assigned_to = user
            task.save()
            
            serializer = self.get_serializer(task)
            return Response({
                'message': f'Task assigned to {user.username}',
                'task': serializer.data
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
