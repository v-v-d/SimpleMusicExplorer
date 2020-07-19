from .test_setup import TestSetup
from ..models import ProductCategory, Product

class TestMerchappSmoke(TestSetup):

    # def test_merchapp_products_urls(self):
    #     response = self.client.get('/api/v1/merch/products/')
    #     self.assertEqual(response.status_code, 200)
    #
    #     for product in Product.objects.all():
    #         response = self.client.get(f'/products/product/{product.pk}/')
    #         self.assertEqual(response.status_code, 200)

    # def test_merchapp_products_pk_urls(self):
    #     response = self.client.get('/api/v1/merch/products/6/')
    #     self.assertEqual(response.status_code, 200)

    def test_merchapp_categories_pk_urls(self):
        response = self.client.get('/api/v1/merch/categories/6/')
        self.assertEqual(response.status_code, 200)

    def test_merchapp_artist_products(self):
        response = self.client.get('/api/v1/merch/artist-products/')
        self.assertEqual(response.status_code, 200)

    def test_merchapp_categories_urls(self):
        response = self.client.get('/api/v1/merch/categories/')
        self.assertEqual(response.status_code, 200)

        # for category in ProductCategory.objects.all():
        #     response = self.client.get(f'/categories/{category.pk}/')
        #     self.assertEqual(response.status_code, 200)




