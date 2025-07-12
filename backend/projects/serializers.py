from rest_framework.serializers import Serializer
from .models import Project

class ProjectSerializer(Serializer):
    name = Serializer.CharField(max_length=255, required=True)
    description = Serializer.CharField(required=True)
    start_date = Serializer.DateTimeField(read_only=True)
    end_date = Serializer.DateTimeField(required=False, allow_null=True)
    updated_at = Serializer.DateTimeField(read_only=True)
    owner = Serializer.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    emoji = Serializer.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    is_active = Serializer.BooleanField(default=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'updated_at', 'owner', 'emoji', 'is_active']