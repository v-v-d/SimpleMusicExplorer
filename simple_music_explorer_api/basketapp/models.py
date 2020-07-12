from django.db import models
from django.db.models import Sum, F

from authapp.models import User
from coreapp.models import Core
from merchapp.models import Product
from musicapp.models import AlbumModel


class BasketItemManager(models.QuerySet):
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
        return self.aggregate(total_summ=Sum(F('quantity') * F('price'), output_field=models.DecimalField())) ['total_summ'] or 0.00


class BasketItemModel(Core):
    album = models.ForeignKey(AlbumModel, blank=True, null=True, on_delete=models.CASCADE)
    merch = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(max_length=3, blank=False, default=1)

    def delete(self, **kwargs):
        return super().delete(force=True)


class BasketManager(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def get_all_from_request(self, request):
        return self.filter(owner=request.user) if request.user.is_authenticated else self.none()

    def get_all_from_request_active(self, request):
        return self.get_all_from_request(request).active()

    def get_from_request_active(self, request):
        for obj in self.get_all_from_request_active(request):
            return obj


class BasketModel(Core):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    basket_items = models.ManyToManyField(BasketItemModel)
    objects = BasketManager.as_manager()

    def delete(self, **kwargs):
        return super().delete(force=True)


