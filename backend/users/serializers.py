from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import ValidationError, UniqueValidator

User = get_user_model()

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This Email is already in use")]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This username already exists")]
    )


    class Meta:
        model = User
        fields = ["email", "username", "password", "confirm_password", 'role']
    
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError({"password": "passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
