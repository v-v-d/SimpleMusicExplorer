import json

from django.urls import reverse
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authapp.models import User


class TestCore(APITestCase):
    def create_and_auth_user(self):
        fake = Faker()
        username = fake.first_name()
        password = fake.password(length=15, special_chars=True)
        email = fake.email()

        url = reverse('user-list')
        data = {'username': username,
                'password': password,
                're_password': password,
                'email': email}

        response = self.client.post(url, data, format='json')
        user = User.objects.get(id=json.loads(response.content.decode()).get('id'))
        user.is_active = True
        user.is_artist = True
        Token.objects.create(user=user)

        self.client.force_authenticate(user=user, token=user.auth_token)
        return user
