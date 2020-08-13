from django.db import models

from coreapp.models import Core, FileModel
from musicapp.models import Artist


class ProductCategory(Core):
    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'

    def __str__(self):
        return self.title


class ProductManager(models.QuerySet):
    def delete(self, **kwargs):
        for obj in self:
            obj.is_active = False
            obj.save()


class Product(Core):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.ManyToManyField(FileModel, blank=True)
    short_desc = models.CharField(verbose_name='Product short description', max_length=60, blank=True)
    price = models.DecimalField(verbose_name='Product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Product quantity in stock', default=0)

    objects = ProductManager.as_manager()

    def __str__(self):
        return f'{self.title} ({self.category.title})'

