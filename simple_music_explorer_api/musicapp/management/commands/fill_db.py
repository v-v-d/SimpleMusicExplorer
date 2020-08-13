import json
from random import randint
from urllib.request import urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from authapp.models import User
from basketapp.models import BasketModel
from coreapp.models import FileModel
from merchapp.models import Product, ProductCategory
from musicapp.models import ArtistAlbum, Artist, AlbumTrack
from orderapp.models import Address, FrozenOrderItem, FrozenTrack, UserOrder, OrderItem

# from paymentapp.models import BillingInformation, Refund

fake = Faker()


def fill_users(qty):
    for _ in range(qty):
        while True:
            try:
                user = User.objects.create_user(
                    username=fake.first_name(),
                    email=fake.email(),
                    password=fake.password()
                )
            except IntegrityError:
                continue
            else:
                if randint(0, 5):
                    user.is_active = True
                break

    User.objects.create_superuser(username='admin', password='admin')


def get_limited_sounds_url_list():
    url = 'https://api.clyp.it/featuredlist/random/?count=100'
    with urlopen(url) as in_stream:
        sounds = json.loads(in_stream.read().decode())
        return [
            sound['Mp3Url']
            for sound in sounds for key, val in sound.items()
            if key == 'Duration' and val < 30
        ]


def get_file(url, file_name, ext):
    with urlopen(url) as in_stream:
        file = ContentFile(in_stream.read())
        file.name = f'{file_name}.{ext}'
        return file


def fill_tracks(qty, artist_id, album_id, sounds_urls):
    for i in range(1, qty + 1):
        track = AlbumTrack.objects.create(
            artist_id=artist_id,
            album_id=album_id,
            title=fake.text(20).strip('.'),
            ordering=i,
        )
        underscored_track_title = '_'.join(track.title.split())
        file = FileModel.objects.create(
            file=get_file(
                sounds_urls.pop(),
                f'audio/{underscored_track_title}_{track.pk}', 'mp3'
            ))
        track.audio_file.add(file)
        track.save()    # For firing calculate_track_duration signal


def fill_albums(artist_id, albums_qty, sounds_urls, max_tracks):
    for _ in range(albums_qty):
        album = ArtistAlbum.objects.create(
            title=fake.text(20).strip('.'),
            price=fake.pydecimal(min_value=0, max_value=10),
            genre=fake.text(10).strip('.'),
            description=fake.text(128),
            artist_id=artist_id
        )
        underscored_album_title = '_'.join(album.title.split())
        file = FileModel.objects.create(
            file=get_file(
                fake.image_url(width=300, height=300),
                f'albums/{underscored_album_title}_{album.pk}', 'jpg'
            ))
        album.image.add(file)

        tracks_qty = randint(1, max_tracks)
        fill_tracks(tracks_qty, artist_id, album.pk, sounds_urls)


def fill_music(user_id, albums_qty, max_tracks, sounds_urls):
    artist = Artist.objects.create(
        user_id=user_id,
        name=fake.text(12).strip('.'),
        location=fake.country(),
        bio=fake.text(400),
        website=fake.domain_name(),
    )
    underscored_artist_name = '_'.join(artist.name.split())
    file = FileModel.objects.create(
        file=get_file(
            fake.image_url(width=300, height=300),
            f'artists/{underscored_artist_name}_{artist.pk}', 'jpg'
        ))
    artist.image.add(file)
    artist.save()
    fill_albums(artist.pk, albums_qty, sounds_urls, max_tracks)


def fill_categories(qty):
    for i in range(qty):
        ProductCategory.objects.create(
            title=fake.word(),
            description=fake.text(250).strip('.'),
            is_active=True,
        )


def get_random_category_id():
    return ProductCategory.objects.order_by('?').first().pk


def fill_products(qty, artist_id):
    for _ in range(qty):
        product = Product.objects.create(
            artist_id=artist_id,
            category_id=get_random_category_id(),
            title=fake.text(12).strip('.'),
            description=fake.text(250).strip('.'),
            short_desc=fake.text(60).strip('.'),
            price=fake.pydecimal(min_value=0, max_value=10),
            quantity=fake.pyint(min_value=1, max_value=20),
        )
        underscored_product_name = '_'.join(product.title.split())
        file = FileModel.objects.create(
            file=get_file(
                fake.image_url(width=300, height=300),
                f'products/{underscored_product_name}_{product.pk}', 'jpg'
            ))
        product.image.add(file)


def get_random_item():
    return Product.objects.order_by('?').first() if randint(0, 1) else ArtistAlbum.objects.order_by('?').first()


def fill_basket(owner_id, items_qty):
    for _ in range(items_qty):
        item = get_random_item()
        qty = 1 if isinstance(item, ArtistAlbum) else fake.pyint(min_value=1, max_value=5)

        BasketModel.objects.create(
            owner_id=owner_id,
            content_object=item,
            quantity=qty
        )


def get_random_status(*statuses):
    return statuses[randint(0, len(statuses)) - 1]


def get_address(user):
    return Address.objects.create(
        user=user,
        first_name=user.username,
        last_name=fake.last_name(),
        email=user.email,
        street_address=fake.street_name(),
        apartment_address=fake.building_number(),
        zip=fake.postcode(),
        city=fake.city()
    )


def get_frozen_order_item(order, origin_item):
    item = FrozenOrderItem.objects.create(
        item_type=origin_item.content_type.name,
        order_number=order.pk,
        artist_name=origin_item.content_object.artist.name,
        title=origin_item.content_object.title,
        price=origin_item.content_object.price
    )
    file = FileModel.objects.filter(id=origin_item.content_object.image.first().pk).first()
    item.image.add(file)
    return item


def fill_frozen_tracks(album, frozen_album):
    for track in album.tracks.all():
        frozen_track = FrozenTrack.objects.create(frozen_album=frozen_album)
        file = FileModel.objects.filter(id=track.audio_file.first().pk).first()
        frozen_track.audio_file.add(file)


def fill_order(artist_id, owner, items_qty):
    order = UserOrder.objects.create(
        artist_id=artist_id,
        owner=owner,
        delivery_address=get_address(owner),
        payment_state=get_random_status('NP', 'P'),
        delivery_status=get_random_status('P', 'C', 'S', 'R')
    )

    for _ in range(items_qty):
        item = get_random_item()

        order_item = OrderItem.objects.create(
            order=order,
            content_object=item,
            quantity=fake.pyint(min_value=1, max_value=5)
        )

        frozen_item = get_frozen_order_item(order, order_item)
        order_item.frozen_order_item = frozen_item
        order_item.save()

        if isinstance(item, ArtistAlbum):
            fill_frozen_tracks(item, frozen_item)


class Command(BaseCommand):
    def handle(self, *args, **options):

        users_qty = 250
        artists_percent = randint(25, 40)
        categories_qty = randint(5, 10)
        baskets_percent = randint(40, 60)
        orders_percent = randint(60, 80)
        max_tracks_per_artist = 10
        max_products_per_artist = 10
        max_basket_items_per_user = 10
        max_order_items_per_user = 10

        fill_users(users_qty)
        fill_categories(categories_qty)

        active_users_ids = User.objects.filter(is_active=True).all().values_list('id', flat=True)
        artists_qty = int(active_users_ids.count() * (artists_percent / 100))

        sounds_urls = get_limited_sounds_url_list()
        artists_ids = active_users_ids[:artists_qty]
        for artist_id in artists_ids:
            albums_qty = randint(0, 5)

            while len(sounds_urls) < albums_qty * max_tracks_per_artist:
                sounds_urls += get_limited_sounds_url_list()

            fill_music(artist_id, albums_qty, max_tracks_per_artist, sounds_urls)

            products_qty = randint(1, max_products_per_artist)
            fill_products(products_qty, artist_id)

        customers_ids = active_users_ids[artists_qty:]
        baskets_qty = int(len(customers_ids) * (baskets_percent / 100))
        customers_ids_with_basket = customers_ids[:baskets_qty]
        for customer_id_with_basket in customers_ids_with_basket:
            customer = User.objects.filter(id=customer_id_with_basket).first()
            basket_items_qty = randint(1, max_basket_items_per_user)
            fill_basket(customer.pk, basket_items_qty)

        orders_qty = int(len(artists_ids) * (orders_percent / 100))
        for idx, (artists_id, customer_id) in enumerate(zip(artists_ids, customers_ids)):
            if idx == orders_qty:
                break
            artist = Artist.objects.filter(user_id=artists_id).first()
            customer = User.objects.filter(id=customer_id).first()
            order_items_qty = randint(1, max_order_items_per_user)
            fill_order(artist.pk, customer, order_items_qty)
