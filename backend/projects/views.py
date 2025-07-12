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
from users.models import User

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(owner=user) | models.Q(project_members=user)
        ).distinct().prefetch_related('tasks', 'project_members')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_task(self, request, pk=None):
        project = self.get_object()
        serializer = TaskCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign_member(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
            return Response({'error': 'Only the owner can add members.'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        elif username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'user_id or username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if user == project.owner:
            return Response({'error': 'Owner is already a member.'}, status=status.HTTP_400_BAD_REQUEST)
        project.project_members.add(user)
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
            return Response({'error': 'Only the owner can remove members.'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        elif username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'user_id or username is required'}, status=status.HTTP_400_BAD_REQUEST)
        if user == project.owner:
            return Response({'error': 'Cannot remove owner from project.'}, status=status.HTTP_400_BAD_REQUEST)
        if user not in project.project_members.all():
            return Response({'error': 'User is not a member.'}, status=status.HTTP_400_BAD_REQUEST)
        project.project_members.remove(user)
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
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
            ).count() if tasks and hasattr(tasks.first(), 'due_date') else 0,
        }
        return Response(stats)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            models.Q(project__owner=user) | 
            models.Q(project__project_members=user)
        ).distinct().select_related('project', 'assigned_to', 'created_by')


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
        task = self.get_object()
        if task.assigned_to != request.user and task.created_by != request.user:
            return Response({'error': 'You do not have permission to complete this task'},
                            status=status.HTTP_403_FORBIDDEN)
        with transaction.atomic():
            if hasattr(task, 'complete_task') and callable(task.complete_task):
                if task.complete_task():
                    serializer = self.get_serializer(task)
                    return Response({
                        'message': 'Task completed successfully',
                        'experience_gained': getattr(task, 'experience_reward', None),
                        'task': serializer.data
                    })
                else:
                    return Response({'error': 'Task could not be completed'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Task model missing complete_task method'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = self.get_queryset().filter(assigned_to=request.user)
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        priority_filter = request.query_params.get('priority')
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def created_by_me(self, request):
        tasks = self.get_queryset().filter(created_by=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        if task.created_by != request.user and task.project.owner != request.user:
            return Response({'error': 'You do not have permission to assign this task'},
                            status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        elif username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'user_id or username is required'}, status=status.HTTP_400_BAD_REQUEST)
        task.assigned_to = user
        task.save()
        serializer = self.get_serializer(task)
        return Response({
            'message': f'Task assigned to {user.username}',
            'task': serializer.data
        })
