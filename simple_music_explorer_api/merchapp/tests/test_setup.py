from rest_framework.test import APITestCase
from django.test.client import Client
from authapp.models import User
from django.core.management import call_command


class TestSetup(APITestCase):


    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        # Set up user
        # self.user = User(email="s_chaban@mail.ru")
        # password = 'SimpleMusic'
        # self.user.set_password(password)
        # self.user.save()
        # Authenticate client with user
        self.client = Client()
        # self.client.login(email=self.user.email, password=password)
        self.superuser = User.objects.create_user('django2', 'django2@geekshop.local', 'geekbrains')

        return super().setUp()


    def tearDown(self):
        call_command(
            'sqlsequencereset', 'musicapp', 'authapp', 'merchapp'
        )