from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum

from authapp.models import User
from coreapp.models import Core
from merchapp.models import Product
from musicapp.models import ArtistModel, AlbumModel, FileModel


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
        return self.filter(active=True)

    def get_queryset(self):
        return super().get_queryset().active()


class ProductOrAlbumToOrder(Core):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # artist = models.CharField(max_length=100)

    artist = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ManyToManyField(FileModel, blank=True)
    short_desc = models.CharField(max_length=60, blank=True, null=True)

    genre = models.CharField(max_length=32, blank=True, null=True)

    objects = ActiveQuerySetManager.as_manager()


class PurchasedTrack(Core):

    album = models.ForeignKey(ProductOrAlbumToOrder, related_name='prod_tracks', null=False, on_delete=models.CASCADE)
    audio_file = models.CharField(max_length=200)
    order = models.SmallIntegerField()

    objects = ActiveQuerySetManager.as_manager()


class OrderManager(models.QuerySet):

    def delete(self, **kwargs):
        for obj in self:
            if obj.payment_state != 'P':
                return super().delete()
            else:
                obj.active = False
                obj.save()


class Orders(Core):
    """Заказ"""

    artist = models.ForeignKey(ArtistModel, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    payment_state = models.CharField(max_length=2, choices=[('NP', 'Not paid '), ('P', 'Paid')])
    total_sum = models.FloatField(default=0)

    objects = OrderManager.as_manager()

    def __str__(self):
        return f'{self.date}'

    def get_total_summ(self):
        return sum(item.get_summ() for item in self.order_items.all())


class OrderItemManager(models.QuerySet):

    def delete(self, **kwargs):
        for obj in self:
            if obj.order.payment_state != 'P':
                return super().delete()


class OrderItem(Core):
    """Товар в заказе"""
    order = models.ForeignKey(Orders, null=False, on_delete=models.CASCADE, related_name='order_items')
    # owner = models.ForeignKey(User, related_name='owner_item', on_delete=models.SET_NULL, null=True) ?
    merch = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    album = models.ForeignKey(AlbumModel, on_delete=models.SET_NULL, blank=True, null=True)
    type_product = models.CharField(max_length=1, choices=[('m', 'merch'), ('t', 'treck')], blank=True)

    fixed_product = models.ForeignKey(ProductOrAlbumToOrder, on_delete=models.SET_NULL, blank=True, null=True, related_name='fixed')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0, null=False, blank=True)
    delivery_status = models.CharField(max_length=2, choices=[('P', 'Processing'), ('C', 'Canceled '), ('S', 'Sent'), ('R', 'Received')], default='P')

    objects = OrderItemManager.as_manager()

    def save(self, *args, **kwargs):
        if self.merch:
            self.type_product = 'm'
        else:
            self.type_product = 't'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}-{self.order.id}'

    def clean(self):
        if not self.album and not self.merch:
            super(OrderItem, self).delete()
        if self.album and self.merch:
            raise ValidationError('Только одно из полей (album_product, merch_product) должно быть заполнено')
        if self.album is None and self.merch is None:
            raise ValidationError('Одно поле должно быть заполнено обязательно, album_product или merch_product')

    def get_summ(self):
        return (self.price or 0) * (self.quantity or 0)
