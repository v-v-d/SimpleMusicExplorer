import json
import random

from django.urls import reverse
from faker import Faker
from rest_framework import status

from simple_music_explorer_api.test_core import TestCore


class UserArtist(TestCore):
    def test_create_retrieve_artist(self):
        # creating fake artist
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

        # retrieving user artist
        request = self.client.get(url)
        result = json.loads(request.content.decode())[0]

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(data['user'], result['user']['id'])


class Artist(TestCore):
    def test_retrieve_update_artist(self):
        user = self.create_and_auth_user()
        self.create_artist(user)

        url = reverse('user-artists')
        artist = self.client.get(url)

        url = reverse('artist_detail', args=[artist.data[0]['id']])
        request = self.client.get(url)
        self.assertEqual(artist.data[0], request.data)

        # update artist
        request = self.client.put(url, data={'name': 'test'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class Albums(TestCore):
    def setUp(self):
        fake = Faker()
        self.user = self.create_and_auth_user()
        self.create_artist(self.user)
        url = reverse('user-artists')
        self.artist = self.client.get(url)

        url = reverse('artist_albums', args=[self.artist.data[0]['id']])
        self.data = {
            'title': fake.first_name(),
            'description': fake.text(),
            'price': round(random.uniform(1, 100), 2),
            'genre': fake.domain_name(),
            'artist': self.artist.data[0]['id']
        }

        self.create_album = self.client.post(url, self.data)

    def test_create_album(self):
        self.assertEqual(self.create_album.status_code, status.HTTP_201_CREATED)

    def test_get_album(self):
        url = reverse('artist_albums', args=[self.artist.data[0]['id']])

        get_album = self.client.get(url)
        self.assertEqual(self.create_album.data, get_album.data[0])

    def test_put_album(self):
        url = reverse('artist_albums', args=[self.artist.data[0]['id']])
        request = self.client.put(url, data={'name': 'test'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        print(1)

    def test_delete_album(self):
        url = reverse('artist_albums', args=[self.create_album.data['id']])
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_patch_album(self):
        url = reverse('artist_albums', args=[self.create_album.data['id']])
        request = self.client.patch(url, data={'name': 'test'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)


class GetAlbums(TestCore):
    def test_get_albums(self):
        self.create_and_auth_user()

        url = reverse('albums')
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')


