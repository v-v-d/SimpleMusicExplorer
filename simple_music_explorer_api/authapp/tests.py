from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authapp.models import User
from faker import Faker

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        basic check to insure djoser works
        """

        fake = Faker()
        url = reverse('user-list')

        username = fake.first_name()
        password = fake.password(length=15, special_chars=True)
        email = fake.free_email()

        data = {
            'username': username,
            'password': password,
            're_password': password,
            'email': email
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, username)
