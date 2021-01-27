import json
import random

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import management

from api_services import models, serializers, enums


class LoginTestCase(APITestCase):

    def setUp(self):
        management.call_command('initializedata')

        self.admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]

        coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        random.shuffle(coaches)
        self.coach = coaches.pop()

        players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        random.shuffle(players)
        self.player = players.pop()

        self.admin_token = Token.objects.create(user=self.admin)
        self.coach_token = Token.objects.create(user=self.coach)
        self.player_token = Token.objects.create(user=self.player)

        self.tournament_url = reverse('tournament-list')

    def test_login_success(self):
        data = {
            "username": "admin@nba.com",
            "password": "1qaz2wsx"
        }
        response = self.client.post('/api/login', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tournament(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.tournament_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tournament_2(self):
        self.client.force_authenticate(user=self.player)
        response = self.client.get(self.tournament_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)