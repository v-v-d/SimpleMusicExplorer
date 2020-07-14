from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum

from authapp.models import User
from coreapp.models import Core
from musicapp.models import ArtistModel


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


class OrderManager(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def get_all_from_request(self, request):
        return self.filter(owner=request.user) if request.user.is_authenticated else self.none()

    def get_all_from_request_active(self, request):
        return self.get_all_from_request(request).active()

    def get_from_request_active(self, request):
        for invoice in self.get_all_from_request_active(request):
            return invoice


class Orders(Core):
    """Заказ"""

    delivery_address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    payment_state = models.CharField(max_length=2, choices=[('NP', 'Not paid '), ('P', 'Paid')])

    objects = OrderManager.as_manager()

    def delete(self, **kwargs):
        return super().delete(force=True)

    def get_summ(self):
        return self.order_item.total_summ()

    def get_quantity(self):
        return self.order_item.total_quantity()


class ProductToOrder(Core):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=60, blank=True)


class AlbumToOrder(Core):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=32)
    artist = models.CharField(max_length=100)


class PurchasedTrack(Core):

    album = models.ForeignKey(AlbumToOrder, related_name='tracks', null=False, on_delete=models.PROTECT)
    audio_file = models.FileField(upload_to='audio')


class OrderItemManager(models.QuerySet):

    def get_queryset(self):
        return super().get_queryset().active()

    def empty(self):
        return self.active().filter(quantity_lte=0).distinct()

    def active(self):
        return self.filter(active=True)

    def get_all_from_request(self, request):
        if request.user.is_authenticated:
            return self.filter(order__owner=request.user)
        return self.none()

    def total_quantity(self):
        return self.aggregate(total_quantity=Sum(F('quantity'), output_field=models.IntegerField()))['total_quantity'] or 0

    def total_summ(self):
        return self.aggregate(total_summ=Sum(F('quantity') * F('price'), output_field=models.DecimalField()))['total_summ'] or 0.00


class OrderItem(Core):
    """Товар в заказе"""
    order = models.ForeignKey(Orders, null=False, on_delete=models.CASCADE, related_name='order_item')
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)
    merch_product = models.ForeignKey(ProductToOrder, on_delete=models.PROTECT, default=None, blank=True, null=True)
    album_product = models.ForeignKey(AlbumToOrder, on_delete=models.PROTECT, default=None, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0, null=False, blank=True)
    delivery_status = models.CharField(max_length=2, choices=[('C', 'Canceled '), ('S', 'Sent'), ('R', 'Received')])

    objects = OrderItemManager.as_manager()

    def delete(self, **kwargs):
        return super().delete(force=True)

    def clean(self):
        if self.album_product and self.merch_product:
            raise ValidationError('Только одно из полей (album_product, merch_product) должно быть заполнено')
        if self.album_product is None and self.merch_product is None:
            raise ValidationError('Одно поле должно быть заполнено обязательно, album_product или merch_product')

    def get_summ(self):
        return (self.price or 0) * (self.quantity or 0)

