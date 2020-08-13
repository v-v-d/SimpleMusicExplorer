from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from authapp.models import User
from coreapp.models import Core
from merchapp.models import Product
from musicapp.models import ArtistAlbum


class BasketModel(Core):
    allowed_object_types = (Product, ArtistAlbum)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    quantity = models.IntegerField(blank=False, default=1)

    def get_current_item(self):
        return self.content_object

    def __str__(self):
        item = self.get_current_item()
        return f'{self.owner}-{item.title}'

    def save(self, *args, **kwargs):
        if isinstance(self.content_object, self.allowed_object_types):
            super().save(*args, **kwargs)
        else:
            raise ValidationError(
                f'Wrong object type. '
                f'Expected {self.allowed_object_types}, got {type(self.content_object)}.'
            )

    @cached_property
    def get_items_cached(self):
        return BasketModel.objects.filter(user_id=self.owner).select_related()

    @property
    def get_product_total_price(self):
        item = self.get_current_item()
        return self.quantity * item.price

    @property
    def get_products_total_quantity_by_user(self):
        return sum([item.quantity for item in self.get_items_cached])

    @property
    def get_products_total_price_by_user(self):
        return sum([item.get_product_total_price for item in self.get_items_cached])

    @staticmethod
    def get_item(pk):
        return __class__.objects.filter(pk=pk).first()



