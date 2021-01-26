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

        admin = list(models.User.objects.filter(role=enums.RoleChoice.ADMIN))[0]

        coaches = list(models.User.objects.filter(role=enums.RoleChoice.COACH))
        random.shuffle(coaches)
        coach = coaches.pop()

        players = list(models.User.objects.filter(role=enums.RoleChoice.PLAYER))
        random.shuffle(players)
        player = players.pop()

        self.admin_token = Token.objects.create(user=admin)
        self.coach_token = Token.objects.create(user=coach)
        self.player_token = Token.objects.create(user=player)

    def test_login_success(self):
        data = {
            "username": "admin@nba.com",
            "password": "1qaz2wsx"
        }
        response = self.client.post('/api/login', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
