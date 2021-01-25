from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from enumfields import EnumField

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

    def __str__(self):
        return self.name


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
    """Database model for a Admin which extends User."""

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
        """"Calculates team points"""

        player_scores = list(self.playerscore_set.all())

        home_team_total = 0
        away_team_total = 0

        for i in range(len(player_scores)):
            player_score = player_scores[i]
            if player_score.player.team == player_score.game.home_team:
                home_team_total += player_score.points
            else:
                away_team_total += player_score.points

        return {
            "home_team_total": home_team_total,
            "away_team_total": away_team_total
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

