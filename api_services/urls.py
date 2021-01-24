from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_services import views

router = DefaultRouter()
router.register('userinfo', views.UserInfoViewSet)

urlpatterns = [
    path('login', views.LoginAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('', include(router.urls)),
]