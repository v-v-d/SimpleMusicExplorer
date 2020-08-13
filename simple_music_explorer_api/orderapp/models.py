from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from authapp.models import User
from coreapp.models import Core, FileModel
from merchapp.models import Product
from musicapp.models import Artist, ArtistAlbum, AlbumTrack


class Address(Core):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    default = models.BooleanField(default=False)


class ActiveQuerySetManager(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def get_queryset(self):
        return super().get_queryset().is_active()


class FrozenOrderItem(Core):
    item_type = models.CharField(max_length=100, blank=False)
    order_number = models.PositiveIntegerField(null=False)
    artist_name = models.CharField(max_length=100, blank=False)
    image = models.ManyToManyField(FileModel, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    objects = ActiveQuerySetManager.as_manager()


class FrozenTrack(Core):
    frozen_album = models.ForeignKey(
        FrozenOrderItem, related_name='frozen_tracks', null=False,
        blank=False, on_delete=models.CASCADE
    )
    audio_file = models.ManyToManyField(FileModel, blank=False)

    objects = ActiveQuerySetManager.as_manager()


class OrderManager(models.QuerySet):
    def delete(self, **kwargs):
        for obj in self:
            if obj.payment_state != 'P':
                return super().delete()
            else:
                obj.is_active = False
                obj.save()


class UserOrder(Core):
    """Order"""

    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    payment_state = models.CharField(max_length=2, choices=[('NP', 'Not paid '), ('P', 'Paid')])
    delivery_status = models.CharField(
        max_length=2, default='P',
        choices=[('P', 'Processing'), ('C', 'Canceled '), ('S', 'Sent'), ('R', 'Received')]
    )

    objects = OrderManager.as_manager()

    def __str__(self):
        return f'{self.date}'

    @property
    def total_cost(self):
        return sum(item.get_sum() for item in self.order_items.all())


class OrderItemManager(models.QuerySet):
    def delete(self, **kwargs):
        for obj in self:
            if obj.order.payment_state != 'P':
                return super().delete()
            else:
                raise ValidationError('Can\'t delete a paid order item.')


class OrderItem(Core):
    """Item in order"""

    order = models.ForeignKey(
        UserOrder, null=False, blank=True, on_delete=models.CASCADE,
        related_name='order_items'
    )

    allowed_object_types = (Product, ArtistAlbum)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=0)
    frozen_order_item = models.ForeignKey(
        FrozenOrderItem, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='frozen'
    )

    objects = OrderItemManager.as_manager()

    def save(self, *args, **kwargs):
        if isinstance(self.content_object, self.allowed_object_types):
            super().save(*args, **kwargs)
        else:
            raise ValidationError(
                f'Wrong object type. '
                f'Expected {self.allowed_object_types}, got {type(self.content_object)}.'
            )

    @property
    def total_cost(self):
        return self.content_object.price * self.quantity

    def __str__(self):
        return f'{type(self.content_object).__name__}-{self.content_object.title} in order {self.order.id}'
