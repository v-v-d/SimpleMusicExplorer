from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from simple_music_explorer_api.merchapp.models import Product, ProductCategory


class TestMerchappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_merchapp_urls(self):
        response = self.client.get('products/')
        self.assertEqual(response.status_code, 200)

        # for category in ProductCategory.objects.all():
        #     response = self.client.get(f'/products/category/{category.pk}/')
        #     self.assertEqual(response.status_code, 200)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',
    #                  'basketapp')
