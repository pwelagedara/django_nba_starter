from django.db import models
from django.conf import settings
from enumfields import EnumField
from django_db_views.db_view import DBView
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from api_services import enums


class UserManager(BaseUserManager):
    """User management"""

    def create_user(self, email, name, role, password=None):
        """Creates a new User in the system"""

        email = self.normalize_email(email)

        user = self.model(email=email, name=name, role=role)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates Super User"""

        user = self.create_user(email, name, enums.RoleChoice.SUPER_ADMIN, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for a User in the system"""

    class Meta:
        ordering = ['id']

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = EnumField(enums.RoleChoice, max_length=20)
    login_count = models.IntegerField(default=0)
    is_online = models.BooleanField(default=False)
    total_time_online = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Team(models.Model):
    """Database model for a Team"""

    name = models.CharField(max_length=255)
    arena_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_team_players(self):
        return list(self.player_set.all())

    def get_average_team_score(self):

        # TODO: Optimize the performance using Database Views
        players = self.get_team_players()

        team_total_score = 0
        for player in players:
            player_scores = player.playerscore_set.all()
            for player_score in player_scores:
                team_total_score += player_score.points

        total_games = len(self.away_team.all()) + len(self.home_team.all())

        return team_total_score / total_games

    def get_team_players_as_users(self):

        players = self.get_team_players()

        users = []
        for player in players:
            users.append(player.user)

        return users


class Player(models.Model):
    """Database model for a Player which extends User"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    height = models.IntegerField(default=0)

    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        null=True
    )


class Admin(models.Model):
    """Database model for a Admin which extends User"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # TODO: Add more model attributes


class Coach(models.Model):
    """Database model for a Coach which extends User"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    team = models.OneToOneField(
        Team,
        on_delete=models.DO_NOTHING,
        null=True
    )


class Tournament(models.Model):
    """Database model for a Tournament"""

    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=255, default="NBA")


class TournamentRound(models.Model):
    """Database model for a Tournament Round"""

    class Meta:
        ordering = ['id']

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.DO_NOTHING
    )

    name = EnumField(enums.TournamentRoundChoice, max_length=20)


class Game(models.Model):
    """Database model for a Game"""

    tournament_round = models.ForeignKey(
        TournamentRound,
        on_delete=models.DO_NOTHING
    )

    home_team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name='home_team'
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name='away_team'
    )

    def get_total_points(self):
        """"Calculates Team points"""

        # Using database view for faster processing
        game_scores = list(self.gamescoresdbview_set.all())

        home_team_total = 0
        away_team_total = 0

        for game_score in game_scores:
            if game_score.team == game_score.game.home_team:
                home_team_total = game_score.team_score
            else:
                away_team_total = game_score.team_score

        return {
            "home_team_total": int(home_team_total),
            "away_team_total": int(away_team_total)
        }

    def get_winning_team(self):
        """Finds the winning team"""

        team_totals = self.get_total_points()
        if team_totals["home_team_total"] > team_totals["away_team_total"]:
            return self.home_team
        return self.away_team


class PlayerScore(models.Model):
    """Database model to store Player Scores"""

    game = models.ForeignKey(
        Game,
        on_delete=models.DO_NOTHING
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING
    )

    points = models.IntegerField(default=0)


class GameScoresDBView(DBView):
    """Database view to store Game scores to aid team total calculation and winner calculation"""

    class Meta:
        managed = False
        db_table = 'api_services_gamescoresdbview'

    game = models.ForeignKey(
        Game,
        on_delete=models.DO_NOTHING
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING
    )

    team_score = models.IntegerField(default=0)

    db_script = """
    SELECT
        row_number() over () AS id, game_id, team_id, SUM(player_score) AS team_score
    FROM
    (
        SELECT
            asps.game_id, asps.player_score, asp.team_id
        FROM
        (
            SELECT game_id, player_id, SUM(points) AS player_score
            FROM api_services_playerscore
            GROUP BY player_id, game_id
            ) asps INNER JOIN api_services_player AS asp ON asps.player_id=asp.user_id
    ) tps GROUP BY game_id, team_id
    """

    view_definition = {
        "django.db.backends.sqlite3": db_script,
        "django.db.backends.postgresql": db_script
    }


class PlayerAverageDBView(DBView):
    """Database view to store Player averages"""

    class Meta:
        managed = False
        db_table = 'api_services_playeraveragedbview'
        ordering = ['player_id']

    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        primary_key=True
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING
    )

    player_average = models.FloatField(default=0.0)

    db_script = """
    SELECT
        apl.player_id, COALESCE(apl.player_average, 0.0) AS player_average,  apisp.team_id
    FROM
    (
        SELECT
            asp.user_id AS player_id, a.player_average AS player_average
        FROM api_services_player AS asp
        LEFT JOIN
        (
            SELECT
                pid AS player_id, ROUND(AVG(player_score),2) AS player_average
            FROM
            (
                SELECT player_id AS pid, SUM(points) AS player_score
                FROM api_services_playerscore
                GROUP BY player_id, game_id
            ) player_totals GROUP BY pid
        ) a ON asp.user_id=a.player_id
    ) apl INNER JOIN api_services_player AS apisp ON apl.player_id=apisp.user_id
    """

    view_definition = {
        "django.db.backends.sqlite3": db_script,
        "django.db.backends.postgresql": db_script
    }


class TeamPlayerScoresDBView(DBView):
    """Database view to store Team scores to aid 90th percentile calculation"""

    class Meta:
        managed = False
        db_table = 'api_services_teamplayerscoresdbview'

    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING
    )

    player_score = models.IntegerField(default=0)

    db_script = """
    SELECT 
        row_number() over () AS id, player_totals.pid AS player_id, pl.team_id,  player_totals.player_score 
    FROM 
    (
        SELECT player_id AS pid, SUM(points) AS player_score 
        FROM api_services_playerscore 
        GROUP BY player_id, game_id
    ) player_totals INNER JOIN api_services_player AS pl ON player_totals.pid=pl.user_id
    """

    view_definition = {
        "django.db.backends.sqlite3": db_script,
        "django.db.backends.postgresql": db_script
    }


