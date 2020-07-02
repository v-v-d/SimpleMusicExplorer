from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum

from authapp.models import User
from merchapp.models import Product
from musicapp.models import AlbumModel


class ActiveModels(models.Model):
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    date_modif = models.DateTimeField(auto_now=True, blank=True)


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


class Order(ActiveModels):
    """Заказ"""

    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)


    owner = models.ForeignKey(User, null=True, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=[], default='', blank=True)  # оплачен, не оплачен

    objects = OrderManager.as_manager()

    def get_summ(self):
        return self.orders_item.total_summ()

    def get_quantity(self):
        return self.orders_item.total_quantity()


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


class OrderItem(ActiveModels):
    """Товар в заказе"""
    album_product = models.ForeignKey(AlbumModel, on_delete=models.PROTECT, blank=True)
    merch_product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0, null=False, blank=True)
    invoices = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='orders_item')
    
    objects = OrderItemManager.as_manager()

    def clean(self):
        if self.album_product and self.merch_product:
            raise ValidationError('Только одно из полей (album_product, merch_product) должно быть заполнено')
        if self.album_product is None and self.merch_product is None:
            raise ValidationError('Одно поле должно быть заполнено обязательно, album_product или merch_product')

    def get_summ(self):
        return (self.price or 0) * (self.quantity or 0)
