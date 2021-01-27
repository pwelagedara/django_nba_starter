import json
import random

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import management

from api_services import models, serializers, enums


def setUpModule():
    management.call_command('initializedata')


class IntegrationTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        print("test data=====")


    def setUp(self):

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

        self.correct_password = '1qaz2wsx'
        self.wrong_password = 'thisisawrongpassword'

    def test_login_failure(self):
        data = {
            "username": self.admin.email,
            "password": self.wrong_password
        }
        response = self.client.post('/api/login', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        data = {
            "username": self.admin.email,
            "password": self.correct_password
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