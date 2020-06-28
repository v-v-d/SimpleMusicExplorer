from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    name = models.CharField(verbose_name='Category name', max_length=64, unique=True)
    description = models.TextField(verbose_name='Category description', blank=True)
    is_active = models.BooleanField(verbose_name='active', db_index=True, default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Product name', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Product short description', max_length=60, blank=True)
    description = models.TextField(verbose_name='Product description', blank=True)
    price = models.DecimalField(verbose_name='Product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Product quantity in stock', default=0)
    is_active = models.BooleanField(verbose_name='active', db_index=True, default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

