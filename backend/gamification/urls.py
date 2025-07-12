from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TeamViewSet, AchievementViewSet, TeamChallengeViewSet,
    LeaderboardViewSet, DashboardViewSet, ActivityLogViewSet, TesttWebhookView 
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('teams', TeamViewSet, basename='team')
router.register('achievements', AchievementViewSet, basename='achievement')
router.register('challenges', TeamChallengeViewSet, basename='teamchallenge')
router.register('leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register('dashboard', DashboardViewSet, basename='dashboard')
router.register('activities', ActivityLogViewSet, basename='activitylog')

urlpatterns = [
    path('', include(router.urls)),
    path('test-webhook/', TesttWebhookView.as_view(), name='test-webhook'),
]
