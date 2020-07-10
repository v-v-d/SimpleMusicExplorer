from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    "serializing products"

    class Meta:
        model = Product
        exclude = ('quantity', 'is_active')


class ProductDetailSerializer(serializers.ModelSerializer):
    "serialization to output the complete data about the product"

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        exclude = ('quantity', 'is_active')