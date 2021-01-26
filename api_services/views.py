import numpy

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api_services import serializers
from api_services import models
from api_services import permissions
from api_services.paginations import DefaultPagination
from api_services import enums


class LoginAPIView(ObtainAuthToken):
    """Login endpoint. Handles creating Authentication Tokens"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /userinfo. Returns User information about the logged in User"""

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
        response = super().retrieve(request, *args, **kwargs)
        data = response.data

        # Format the response to have the tournament_winner. If an error occurs do nothing
        try:
            # TODO: Use a model mapper
            tournament_rounds = data['tournament_rounds']
            data['tournament_winner'] = data['tournament_rounds'][3]['games'][0]['winning_team']
            del data['tournament_rounds']
            data['tournament_rounds'] = tournament_rounds
        except IndexError:
            pass

        return Response(data)


class TeamViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Supports GET /team and GET /team/{id} endpoints"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permissions.IsSuperAdmin | permissions.IsAdmin | permissions.IsCoach
    )

    queryset = models.Team.objects.none()
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BasicTeamSerializer
        return serializers.DetailedTeamSerializer

    def get_queryset(self):
        if self.request.user.role == enums.RoleChoice.SUPER_ADMIN or self.request.user.role == enums.RoleChoice.ADMIN:
            return models.Team.objects.all()
        else:
            coach = models.Coach.objects.get(pk=self.request.user.id)
            return models.Team.objects.filter(pk=coach.team.id)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        return Response(data)


class PlayerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Supports GET /player and GET /player/{id} endpoints"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permissions.IsSuperAdmin | permissions.IsAdmin | permissions.IsCoach
    )

    queryset = models.Team.objects.none()
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        return serializers.BasicPlayerAverageDBViewSerializer

    def get_queryset(self):
        if self.request.user.role == enums.RoleChoice.COACH:
            coach = models.Coach.objects.get(pk=self.request.user.id)
            if self.action == 'list':
                top_players = self.request.GET.get('top_players', False)

                if top_players:

                    team_player_scores = models.TeamPlayerScoresDBView.objects.filter(team=coach.team.id)
                    scores = []
                    for team_player_score in team_player_scores:
                        scores.append(team_player_score.player_score)

                    # Calculate 90th percentile using numpy
                    p_90 = numpy.percentile(scores, 90)

                    return models.PlayerAverageDBView.objects.filter(team=coach.team.id, player_average__gte=p_90)

            return models.PlayerAverageDBView.objects.filter(team=coach.team.id)
        else:
            return models.PlayerAverageDBView.objects.all()

    # noinspection PyMethodMayBeStatic
    def __normalize_response(self, data):

        # TODO: Use a model mapper
        data['id'] = data['player']['user']['id']
        data['name'] = data['player']['user']['name']
        data['height'] = data['player']['height']
        player_average = data['player_average']
        team = data['team']

        del data['player']
        del data['player_average']
        del data['team']

        data['player_average'] = player_average
        data['team'] = team

        return data

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for data in response.data['results']:
            self.__normalize_response(data)

        return Response(response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        self.__normalize_response(response.data)
        return Response(response.data)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Supports GET /admin/user and GET /admin/user/{id} endpoints"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permissions.IsSuperAdmin | permissions.IsAdmin
    )

    queryset = models.User.objects.all()
    pagination_class = DefaultPagination
    serializer_class = serializers.DetailedUserSerializer
