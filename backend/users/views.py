from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.conf import settings

from .serializers import RegisterSerializer, UserListSerializer

User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data.get("access")
            refresh = response.data.get("refresh")
            del response.data["refresh"]
            response.set_cookie(
                key="access_token",
                value=access,
                httponly=False,
                secure=False,
                samesite='Lax',
                path='/'
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/api/token/refresh/'
            )
        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        if refresh is None:
            return Response({"error": "Refresh token is not provided."}, status=400)
        request.data["refresh"] = refresh
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"Message": "Logged out successfully"})
        response.delete_cookie(
            key="access_token",
            path="/",
        )
        response.delete_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            path="/api/token/refresh/",
        )
        return response

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        exp = getattr(user, "exp_points", 0)
        level = exp // 100 + 1
        experience = exp % 100
        experience_to_next = 100 - experience
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.get_full_name() or user.username,
            "email": user.email,
            "avatar": getattr(user, "avatar", "🧑‍💻"),
            "level": level,
            "experience": experience,
            "experienceToNext": experience_to_next,
            "currentStreak": getattr(user, "current_streak", 0),
            "points": getattr(user, "points", 0),
        })


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "avatar"]

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
