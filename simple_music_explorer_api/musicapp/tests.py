from django.urls import reverse
from rest_framework import status
from simple_music_explorer_api.test_core import TestCore

from faker import Faker


class Artist(TestCore):
    def test_create_artist(self):
        fake = Faker()
        user = self.create_and_auth_user()

        url = reverse('user-artists')

        data = {
            'user': user.id,
            'name': fake.company(),
            'location': fake.address(),
            'bio': fake.text(),
            'website': fake.domain_name()
        }

        request = self.client.post(url, data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class GetAlbums(TestCore):
    def test_get_albums(self):
        self.create_and_auth_user()

        url = reverse('albums')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')


