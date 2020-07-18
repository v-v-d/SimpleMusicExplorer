from rest_framework import serializers

from musicapp.serializers import ArtistSerializer, FileSerializer
from .models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    """Сериализация продукта"""
    artist = ArtistSerializer()
    image = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'artist', 'category', 'image', 'short_desc', 'price')


class CategoryListViewSerializer(serializers.ModelSerializer):
    """Сериализация категории"""

    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'description')


class ProductCreateSerializer(serializers.ModelSerializer):
    """Сериализация создание продукта"""
    title = serializers.CharField(max_length=100, required=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'image', 'short_desc', 'price', 'quantity')

    def create(self, validated_data):
        product, _ = Product.objects.update_or_create(**validated_data)
        return product


