from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum

from authapp.models import User
from coreapp.models import Core


class Address(Core):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    default = models.BooleanField(default=False)


class OrderManager(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def get_all_from_request(self, request):
        return self.filter(owner=request.user)

    def get_all_from_request_active(self, request):
        return self.get_all_from_request(request).active()

    def get_from_request_active(self, request):
        for invoice in self.get_all_from_request_active(request):
            return invoice


class Order(Core):
    """Заказ"""

    delivery_address = models.ForeignKey(Address, blank=True, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, null=True, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[])

    objects = OrderManager.as_manager()

    def get_summ(self):
        return self.order_item.total_summ()

    def get_quantity(self):
        return self.order_item.total_quantity()


class OrderItemManager(models.QuerySet):

    def get_queryset(self):
        return super().get_queryset().active()

    def empty(self):
        return self.active().filter(quantity_lte=0).distinct()

    def active(self):
        return self.filter(is_active=True)

    def get_all_from_request(self, request):
        if request.user.is_authenticated:
            return self.filter(invoices__owner=request.user)
        return self.none()

    def total_quantity(self):
        return self.aggregate(total_quantity=Sum(F('quantity'), output_field=models.IntegerField()))['total_quantity'] or 0

    def total_summ(self):
        return self.aggregate(total_summ=Sum(F('quantity') * F('price'), output_field=models.DecimalField()))['total_summ'] or 0.00


class ProductToOrder(Core):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=60, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class AlbumToOrder(Core):

    price = models.FloatField(default=0, null=False)
    genre = models.CharField(max_length=32)
    artist = models.CharField(max_length=100)


class PurchasedTrack(Core):

    album = models.ForeignKey(AlbumToOrder, related_name='tracks', null=False, on_delete=models.PROTECT)
    audio_file = models.FileField(upload_to='audio')


class OrderItem(Core):
    """Товар в заказе"""
    merch_product = models.ForeignKey(ProductToOrder, on_delete=models.PROTECT, default=None, blank=True, null=True)
    album_product = models.ForeignKey(AlbumToOrder, on_delete=models.PROTECT, default=None, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0, null=False, blank=True)
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='order_item')

    objects = OrderItemManager.as_manager()

    def clean(self):
        if self.album_product and self.merch_product:
            raise ValidationError('Только одно из полей (album_product, merch_product) должно быть заполнено')
        if self.album_product is None and self.merch_product is None:
            raise ValidationError('Одно поле должно быть заполнено обязательно, album_product или merch_product')

    def get_summ(self):
        return (self.price or 0) * (self.quantity or 0)
