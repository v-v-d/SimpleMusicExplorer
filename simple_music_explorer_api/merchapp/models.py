from django.db import models

# Create your models here.
from coreapp.models import Core
from musicapp.models import ArtistModel


class ProductCategory(Core):
    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.title


class Product(Core):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Product short description', max_length=60, blank=True)
    price = models.DecimalField(verbose_name='Product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Product quantity in stock', default=0)

    def __str__(self):
        return f'{self.title} ({self.category.title})'

