import random

from rest_framework.test import APITestCase
from rest_framework import status
from django.core import management
from rest_framework.authtoken.models import Token

from api_services import models, enums


# Use the management command to load the data
def setUpModule():
    management.call_command('initializedata')


class LoginTestCase(APITestCase):
    """Test the login endpoint"""

    def setUp(self):
        self.correct_password = '1qaz2wsx'
        self.wrong_password = 'thisisawrongpassword'
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/login'
        self.user = models.User.objects.create_user(
            "test@nba.com",
            "John Doe",
            enums.RoleChoice.COACH,
            self.correct_password
        )

    def test_login_success(self):
        """Test login success"""

        data = {
            "username": self.user.email,
            "password": self.correct_password
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('token' in response.data.keys(), True)

    def test_login_failure(self):
        """Test login failure when a wrong password is entered"""

        data = {
            "username": self.user.email,
            "password": self.wrong_password
        }
        response = self.client.post(self.url, data)

        # Must be 401 Unauthorized. But Django seems to send a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserinfoCase(APITestCase):
    """Test GET /userinfo endpoint"""

    def setUp(self):
        self.email = "test@nba.com"
        self.name = "John Doe"
        self.role = enums.RoleChoice.COACH
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/userinfo/'
        self.user = models.User.objects.create_user(
            self.email,
            self.name,
            self.role,
            '1qaz2wsx'
        )

        self.user.login_count = 20
        self.user.total_time_online = 1000
        self.user.is_online = 1
        self.user.save()

    def test_get_userinfo_success(self):
        """Test success response"""

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual('id' in response.data.keys(), True)
        self.assertEqual('email' in response.data.keys(), True)
        self.assertEqual('name' in response.data.keys(), True)
        self.assertEqual('role' in response.data.keys(), True)
        self.assertEqual(response.data['email'], self.email)
        self.assertEqual(response.data['name'], self.name)
        self.assertEqual(response.data['role'], self.role.name)

    def test_get_userinfo_authentication_failure(self):
        """Test failure response without authentication"""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('detail' in response.data.keys(), True)


# noinspection DuplicatedCode
class TournamentTestCase(APITestCase):
    """Test GET /tournament endpoints"""

    def setUp(self):
        self.admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]
        self.coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        self.players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        self.tournament = models.Tournament.objects.get()
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/tournament/'
        self.invalid_token = 'thisisaninvalidtoken'
        self.invalid_tournament_id = '1234567890'
        random.shuffle(self.coaches)
        random.shuffle(self.players)
        self.coach = self.coaches[0]
        self.player = self.players[0]

    def test_get_tournament_authentication_failure(self):
        """Test an authentication failure"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_tournament_admin_success(self):
        """Test successful response for an admin. An admin is allowed to access this endpoint"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_tournament_coach_success(self):
        """Test successful response for coach"""

        token = Token.objects.create(user=self.coach)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_tournament_player_success(self):
        """Test successful response for player"""

        token = Token.objects.create(user=self.player)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_tournament_by_id_success(self):
        """Test successful response for GET /tournament/{id} endpoint"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.tournament.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('id' in response.data.keys(), True)
        self.assertEqual('name' in response.data.keys(), True)
        self.assertEqual('tournament_winner' in response.data.keys(), True)
        self.assertEqual('tournament_rounds' in response.data.keys(), True)

    def test_get_tournament_by_id_404_failure(self):
        """Test a 404 response for GET /tournament/{id} endpoint"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.invalid_tournament_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('detail' in response.data.keys(), True)


# noinspection DuplicatedCode
class TeamTestCase(APITestCase):
    """Test GET /team endpoints"""

    def setUp(self):
        self.admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]
        self.coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        self.players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        self.teams = list(models.Team.objects.all())
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/team/'
        self.invalid_token = 'thisisaninvalidtoken'
        self.invalid_team_id = '1234567890'
        random.shuffle(self.coaches)
        random.shuffle(self.players)
        random.shuffle(self.teams)
        self.coach = self.coaches[0]
        self.player = self.players[0]
        self.team = self.teams[0]

    def test_get_team_authentication_failure(self):
        """Test GET /team endpoint authentication failure by entering an invalid token"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_team_admin_success(self):
        """Test successful response for an Admin User"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_team_coach_success(self):
        """Test successful response for a Coach"""

        token = Token.objects.create(user=self.coach)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_team_player_failure(self):
        """Test whether a player gets a 403 error as he/ she is not allowed in"""

        token = Token.objects.create(user=self.player)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_team_by_id_success(self):
        """Test a successful team details response"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.team.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('id' in response.data.keys(), True)
        self.assertEqual('name' in response.data.keys(), True)
        self.assertEqual('arena_name' in response.data.keys(), True)
        self.assertEqual('team_average' in response.data.keys(), True)
        self.assertEqual('team_players' in response.data.keys(), True)

    def test_get_team_by_id_404_failure(self):
        """Test a 404 team details response using an invalid Team Id"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.invalid_team_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('detail' in response.data.keys(), True)


# noinspection DuplicatedCode
class PlayerTestCase(APITestCase):
    """Test GET /player endpoints"""

    def setUp(self):
        self.admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]
        self.coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        self.players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/player/'
        self.invalid_token = 'thisisaninvalidtoken'
        self.invalid_player_id = '1234567890'
        random.shuffle(self.coaches)
        random.shuffle(self.players)
        self.coach = self.coaches[0]
        self.player = self.players[0]

    def test_get_player_authentication_failure(self):
        """Test GET /player authentication failure by entering an invalid token"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_player_admin_success(self):
        """Test to see if an Admin can access the endpoint"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_player_coach_success(self):
        """Test to see if a Coach can access the endpoint"""

        token = Token.objects.create(user=self.coach)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_player_coach_90th_percentile_success(self):
        """Test to see if a Coach can access the 90th percentile"""

        token = Token.objects.create(user=self.coach)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}?top_players=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_player_player_failure(self):
        """Test to see if a Player cannot access"""

        token = Token.objects.create(user=self.player)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_player_by_id_success(self):
        """Test to see if we can get a 200 OK GET /player/{id} response"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.player.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('id' in response.data.keys(), True)
        self.assertEqual('name' in response.data.keys(), True)
        self.assertEqual('height' in response.data.keys(), True)
        self.assertEqual('player_average' in response.data.keys(), True)
        self.assertEqual('team' in response.data.keys(), True)

    def test_get_player_by_id_404_failure(self):
        """Test to see if we can get 404 NOT FOUND GET /player/{id} response"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.invalid_player_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('detail' in response.data.keys(), True)


# noinspection DuplicatedCode
class AdminUserTestCase(APITestCase):
    """Test stats endpoints. Only accessible by the Admin"""

    def setUp(self):
        self.admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]
        self.coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        self.players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        # FIXME: Do not hardcode the URL. Use reverse
        self.url = '/api/admin/user/'
        self.invalid_token = 'thisisaninvalidtoken'
        self.invalid_user_id = '1234567890'
        random.shuffle(self.coaches)
        random.shuffle(self.players)
        self.coach = self.coaches[0]
        self.player = self.players[0]

    def test_get_admin_user_authentication_failure(self):
        """Test stats endpoints for 401 responses by entering an invalid token"""

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_admin_user_admin_success(self):
        """Test success response for an Admin"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('count' in response.data.keys(), True)
        self.assertEqual('results' in response.data.keys(), True)

    def test_get_admin_user_coach_failure(self):
        """Test failure response for a Coach"""

        token = Token.objects.create(user=self.coach)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_admin_user_player_failure(self):
        """Test failure response for a Player"""

        token = Token.objects.create(user=self.player)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('detail' in response.data.keys(), True)

    def test_get_admin_user_by_id_success(self):
        """Test success response details endpoint"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.player.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('id' in response.data.keys(), True)
        self.assertEqual('email' in response.data.keys(), True)
        self.assertEqual('name' in response.data.keys(), True)
        self.assertEqual('is_active' in response.data.keys(), True)
        self.assertEqual('is_staff' in response.data.keys(), True)
        self.assertEqual('role' in response.data.keys(), True)
        self.assertEqual('login_count' in response.data.keys(), True)
        self.assertEqual('is_online' in response.data.keys(), True)
        self.assertEqual('total_time_online' in response.data.keys(), True)

    def test_get_admin_user_by_id_404_failure(self):
        """Expect a 404 not found for an invalid User Id"""

        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(f"{self.url}{self.invalid_user_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('detail' in response.data.keys(), True)
