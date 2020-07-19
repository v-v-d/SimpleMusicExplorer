from random import randint
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand
from faker import Faker

from merchapp.models import Product, ProductCategory
from musicapp.models import ArtistModel
from authapp.models import User

fake = Faker()


def fill_users(qty):
    for _ in range(qty):
        while True:
            try:
                User.objects.create_user(
                    username=fake.first_name(),
                    email=fake.email(),
                    password=fake.password()
                )
                break
            except IntegrityError:
                continue


def fill_products(artist_id, qty, category_id):
    for _ in range(qty):
        Product.objects.create(
            category_id=category_id,
            title=fake.text(12).strip('.'),
            price=fake.pydecimal(min_value=0, max_value=10),
            quantity=fake.pyint(min_value=1, max_value=20),
            artist_id=artist_id
        )


def fill_categories_with_products(artist_id, qty):
    for i in range(qty):
        category = ProductCategory(
            title=fake.word(),
            description=fake.text(250).strip('.'),
            active=True,
        )
        category.save()

        products_qty = fake.pyint(min_value=1, max_value=10)
        fill_products(artist_id, products_qty, category.pk)


def fill_music(user_id, categories_qty):
    artist = ArtistModel(
        user_id=user_id,
        name=fake.text(12).strip('.'),
        location=fake.country(),
        bio=fake.text(400),
        website=fake.domain_name()
    )
    artist.save()

    fill_categories_with_products(artist.pk, categories_qty)


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_qty = 50
        artists_percent = 30

        fill_users(users_qty)

        users_ids = User.objects.all().values_list('id', flat=True)
        step = int(users_qty / (users_qty * (artists_percent / 100)))
        artists_ids = users_ids[::step]

        for artist_id in artists_ids:
            categories_qty = randint(1, 7)
            fill_music(artist_id, categories_qty)