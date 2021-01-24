from django.core.management.base import BaseCommand, CommandError
import random
import names
from copy import deepcopy

from api_services import models
from api_services import enums
from api_services import constants


class Command(BaseCommand):
    help = "Initializes the data for a single tournament"

    # noinspection PyMethodMayBeStatic
    def __create_user(self, email, role):
        """Helper function to create a User"""

        user = models.User.objects.create_user(
            email,
            names.get_full_name(gender='male'),
            role,
            constants.PASSWORD
        )

        user.login_count = random.randint(0, 1000)
        user.total_time_online = random.randint(0, 1000)
        user.is_online = random.randint(0, 1)
        user.save()

        return user

    # noinspection PyMethodMayBeStatic
    def __play_tournament_round(self, tournament_round, teams):
        """Helper function to play a Tournament Round"""

        teams_copy = deepcopy(teams)

        if len(teams_copy) % 2:
            raise CommandError(constants.EXCEPTION_MESSAGE_INVALID_TEAMS)

        tournament_round_winners = []

        for i in range(len(teams_copy)//2):
            home_team = teams_copy.pop()
            away_team = teams_copy.pop()

            game = models.Game.objects.create(
                tournament_round=tournament_round,
                home_team=home_team,
                away_team=away_team
            )

            home_team_players = list(home_team.player_set.all())
            away_team_players = list(away_team.player_set.all())
            all_players = home_team_players + away_team_players
            number_of_scoring_shots = random.randint(5, 25)

            for j in range(number_of_scoring_shots):
                models.PlayerScore.objects.create(
                    game=game,
                    player=random.choice(all_players),
                    points=random.randint(1, 3)
                )

            winning_team = game.get_winning_team()
            tournament_round_winners.append(winning_team)

        return tournament_round_winners

    def handle(self, *args, **options):

        # Generate 1 Admin User
        admin = self.__create_user("admin@nba.com", enums.RoleChoice.ADMIN)
        models.Admin.objects.create(user=admin)

        team_names = deepcopy(constants.TEAM_NAMES)
        arena_names = deepcopy(constants.ARENA_NAMES)

        random.shuffle(team_names)
        random.shuffle(arena_names)

        # Generate 16 Teams
        for i in range(16):
            team = models.Team.objects.create(name=team_names.pop(), arena_name=arena_names.pop())
            coach = self.__create_user(f"coach{i + 1}@nba.com", enums.RoleChoice.COACH)
            models.Coach.objects.create(user=coach, team=team)

            for j in range(10):
                player = self.__create_user(f"player{i + 1}{j + 1}@nba.com", enums.RoleChoice.PLAYER)
                models.Player.objects.create(user=player, height=random.randint(60, 96), team=team)

        # Create the Tournament
        tournament = models.Tournament.objects.create(name="NBA College Basketball Tournament")

        all_teams = list(models.Team.objects.all())
        random.shuffle(all_teams)

        # First Round
        first_round = models.TournamentRound.objects.create(tournament=tournament, name=enums.TournamentRoundChoice.FIRST_ROUND)
        first_round_winners = self.__play_tournament_round(first_round, all_teams)

        # Second Round
        second_round = models.TournamentRound.objects.create(tournament=tournament, name=enums.TournamentRoundChoice.QUARTER_FINALS)
        second_round_winners = self.__play_tournament_round(second_round, first_round_winners)

        # Third Round
        third_round = models.TournamentRound.objects.create(tournament=tournament, name=enums.TournamentRoundChoice.SEMI_FINALS)
        third_round_winners = self.__play_tournament_round(third_round, second_round_winners)

        # Finals
        final_round = models.TournamentRound.objects.create(tournament=tournament, name=enums.TournamentRoundChoice.FINALS)
        final_round_winner = self.__play_tournament_round(final_round, third_round_winners)

        print(f"{final_round_winner[0]} wins the Tournament")








