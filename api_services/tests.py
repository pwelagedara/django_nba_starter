import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core import management

from api_services import models, serializers


class LoginTestCase(APITestCase):

    def setUp(self):
        management.call_command('initializedata')

    def test_login_success(self):
        data = {
            "username": "admin@nba.com",
            "password": "1qaz2wsx"
        }
        response = self.client.post('/api/login', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
