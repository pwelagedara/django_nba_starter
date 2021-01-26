from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_services import views

router = DefaultRouter()
router.register('userinfo', views.UserInfoViewSet)
router.register('tournament', views.TournamentViewSet)
router.register('team', views.TeamViewSet)
router.register('player', views.PlayerViewSet)
router.register('admin/user', views.UserViewSet)

urlpatterns = [
    path('login', views.LoginAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('', include(router.urls)),
]