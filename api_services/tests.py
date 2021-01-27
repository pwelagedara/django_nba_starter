import random

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import management

from api_services import models, enums


# Use the management command to load the data
def setUpModule():
    management.call_command('initializedata')


class LoginTestCase(APITestCase):

    correct_password = '1qaz2wsx'
    wrong_password = 'thisisawrongpassword'
    url = '/api/login'

    def setUp(self):
        # print(reverse('LoginAPIView'))
        self.user = models.User.objects.create_user(
            "test@nba.com",
            "John Doe",
            enums.RoleChoice.COACH,
            self.correct_password
        )

    def test_login_success(self):
        data = {
            "username": self.user.email,
            "password": self.correct_password
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('token')), True)

    def test_login_failure(self):
        data = {
            "username": self.user.email,
            "password": self.wrong_password
        }
        response = self.client.post(self.url, data)

        # Must be 401 Unauthorized. But Django seems to send a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserinfoCase(APITestCase):

    email = "test@nba.com"
    name = "John Doe"
    role = enums.RoleChoice.COACH
    url = '/api/userinfo/'

    def setUp(self):
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
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('id')), True)
        self.assertEqual(bool(response.data.get('email')), True)
        self.assertEqual(bool(response.data.get('name')), True)
        self.assertEqual(bool(response.data.get('role')), True)
        self.assertEqual(response.data.get('email'), self.email)
        self.assertEqual(response.data.get('name'), self.name)
        self.assertEqual(response.data.get('role'), self.role.name)

    def test_get_userinfo_authentication_failure(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(bool(response.data.get('detail')), True)


class TournamentTestCase(APITestCase):

    admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]
    coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
    players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
    tournament = models.Tournament.objects.get()
    url = reverse('tournament-list')
    invalid_token = 'thisisaninvalidtoken'
    invalid_tournament_id = '1234567890'

    def setUp(self):
        self.coach = random.choice(self.coaches)
        self.player = random.choice(self.players)
        self.admin_token = Token.objects.create(user=self.admin)
        self.coach_token = Token.objects.create(user=self.coach)
        self.player_token = Token.objects.create(user=self.player)

    def test_get_tournament_authentication_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(bool(response.data.get('detail')), True)

    # noinspection DuplicatedCode
    def test_get_tournament_admin_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('count')), True)
        self.assertEqual(bool(response.data.get('results')), True)

    # noinspection DuplicatedCode
    def test_get_tournament_coach_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach_token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('count')), True)
        self.assertEqual(bool(response.data.get('results')), True)

    # noinspection DuplicatedCode
    def test_get_tournament_player_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.player_token.key)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('count')), True)
        self.assertEqual(bool(response.data.get('results')), True)

    def test_get_tournament_by_id_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(f"{self.url}{self.tournament.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bool(response.data.get('id')), True)
        self.assertEqual(bool(response.data.get('name')), True)
        self.assertEqual(bool(response.data.get('tournament_winner')), True)
        self.assertEqual(bool(response.data.get('tournament_rounds')), True)

    def test_get_tournament_by_id_404_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(f"{self.url}{self.invalid_tournament_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(bool(response.data.get('detail')), True)


# Team - Admin, Coach, No Player( 403 with no access)
# Player - Admin, Coach( with top_players query param), No Player( 403 with no access)

