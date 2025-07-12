from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

User = get_user_model()

# NOTE: User Registration View
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# HACK: For protected endpoint testing purposes only
# TODO: Delete later once tested
class HelloView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}"})

# NOTE: Login View using JWT Auth returns Access Token as JSON and Refresh Token as Cookie
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # NOTE: This calls the TokenObtainPairView to generate a new Access Token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh = response.data["refresh"]
            del response.data["refresh"]
        
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=refresh,
                httponly=True,
                secure=False, # NOTE: Set this to "True" in Production
                samesite='Lax',
                path='/api/token/refresh/',
            )

        return response

# NOTE: View For Token Refresh using Cookies
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
        
        if refresh is None:
            return Response({"error": "Refresh token is not provided."}, status=400)
        
        request.data["refresh"] = refresh

        # NOTE: Generates and Returns a new Access Token
        return super().post(request, *args, **kwargs)

# NOTE: This Logout view deletes the Refresh Token Cookie
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"Message": "Logged out succesfully"})
        response.delete_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            path='/api/token/refresh/',
        )
        return response