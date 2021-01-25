from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api_services import serializers
from api_services import models
from api_services import permissions
from api_services.pagination import DefaultPagination


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


class TournamentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Supports GET /tournament and GET /tournament/{id} endpoints"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permissions.IsSuperAdmin | permissions.IsAdmin | permissions.IsCoach | permissions.IsPlayer
    )

    queryset = models.Tournament.objects.all()
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BasicTournamentSerializer
        return serializers.TournamentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        try:
            data['tournament_winner'] = data['tournament_rounds'][3]['games'][0]['winning_team']
        except IndexError:
            pass

        return Response(data)




