from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from authapp.models import User
from coreapp.models import Core
from merchapp.models import Product
from musicapp.models import AlbumModel


class BasketModel(Core):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(AlbumModel, blank=True, null=True, on_delete=models.CASCADE)
    merch = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    type_product = models.CharField(max_length=1, choices=[('m', 'merch'), ('t', 'treck')], blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(blank=False, default=1)

    def __str__(self):
        if self.type_product == 'm':
            return f'{self.owner}-{self.merch.title}'
        else:
            return f'{self.owner}-{self.album.title}'

    def save(self, *args, **kwargs):
        if self.merch:
            self.type_product = 'm'
            self.price = self.merch.price
        else:
            self.type_product = 't'
            self.price = self.album.price

        super().save(*args, **kwargs)

    def clean(self):
        if self.album and self.merch:
            raise ValidationError('Только одно из полей (album, merch) должно быть заполнено')
        if self.album is None and self.merch is None:
            raise ValidationError('Одно поле должно быть заполнено обязательно, album или merch')

    @cached_property
    def get_items_cached(self):
        return BasketModel.objects.filter(user_id=self.owner).select_related()

    @property
    def get_product_total_price(self):
        return self.quantity * self.price

    @property
    def get_products_total_quantity_by_user(self):
        return sum([item.quantity for item in self.get_items_cached])

    @property
    def get_products_total_price_by_user(self):
        return sum([item.get_product_total_price for item in self.get_items_cached])

    @staticmethod
    def get_item(pk):
        return __class__.objects.filter(pk=pk).first()



