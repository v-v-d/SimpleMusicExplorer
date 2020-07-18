from django.core.management.base import BaseCommand
from faker import Faker

from merchapp.models import Product, ProductCategory

fake = Faker()


def fill_products(qty, category_id):
    for _ in range(qty):
        Product.objects.create(
            category_id=category_id,
            title=fake.text(12).strip('.'),
            price=fake.pydecimal(min_value=0, max_value=10),
            quantity=fake.pyint(min_value=1, max_value=20),

        )


def fill_categories_with_products(qty):
    for i in range(qty):
        category = ProductCategory(
            title=fake.word(),
            description=fake.text(250).strip('.'),
        )
        category.save()

        products_qty = fake.pyint(min_value=1, max_value=10)
        fill_products(products_qty, category.pk)


class Command(BaseCommand):
    def handle(self, *args, **options):

        categories_qty = 7
        fill_categories_with_products(categories_qty)