from rest_framework import serializers
from drf_enum_field.serializers import EnumFieldSerializerMixin

from api_services import models


class UserInfoSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    """Serializes a User object for GET /userinfo endpoint"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'role')


class TeamSerializer(serializers.ModelSerializer):
    """Serializes a Team"""

    class Meta:
        model = models.Team
        fields = ('id', 'name')


class GameSerializer(serializers.ModelSerializer):
    """Serializes a Game"""

    class Meta:
        model = models.Game
        fields = ('home_team', 'away_team', 'winning_team', 'scores')

    home_team = TeamSerializer()
    away_team = TeamSerializer()
    winning_team = TeamSerializer(source='get_winning_team')
    scores = serializers.DictField(source='get_total_points')


class TournamentRoundSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    """Serializes a Tournament Round"""

    class Meta:
        model = models.TournamentRound
        fields = ('name', 'games')

    games = GameSerializer(source='game_set', many=True)


class TournamentSerializer(serializers.ModelSerializer):
    """Serializes a Tournament object"""

    class Meta:
        model = models.Tournament
        fields = ('id', 'name', 'tournament_rounds')

    tournament_rounds = TournamentRoundSerializer(source='tournamentround_set', many=True)


class BasicTournamentSerializer(EnumFieldSerializerMixin, serializers.ModelSerializer):
    """Serializes a basic Tournament object"""

    class Meta:
        model = models.Tournament
        fields = ('id', 'name')


class BasicTeamSerializer(serializers.ModelSerializer):
    """Serializes a Team for GET /team endpoint"""

    class Meta:
        model = models.Team
        fields = ('id', 'name', 'arena_name')


class BasicUserSerializer(serializers.ModelSerializer):
    """Serializes a User for GET /team/{id} endpoint"""

    class Meta:
        model = models.User
        fields = ('id', 'name')


class DetailedTeamSerializer(serializers.ModelSerializer):
    """Serializes a Team for GET /team/{id} endpoint"""

    class Meta:
        model = models.Team
        fields = ('id', 'name', 'arena_name', 'team_average', 'team_players')

    team_average = serializers.FloatField(source='get_average_team_score')
    team_players = serializers.ListSerializer(source='get_team_players_as_users', child=BasicUserSerializer())
