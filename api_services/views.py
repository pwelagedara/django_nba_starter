from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api_services import serializers
from api_services import  models


class LoginAPIView(ObtainAuthToken):
    """Login endpoint. Handles creating Authentication Tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """User Info endpoint. Returns User information about the logged in User"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = serializers.UserInfoSerializer
    queryset = models.User.objects.none()

    def list(self, request, *args, **kwargs):
        """Custom list method"""

        queryset = models.User.objects.filter(id=self.request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        return Response(data[0])




