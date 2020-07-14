from rest_framework import serializers

from musicapp.serializers import ArtistSerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализация продукта"""
    seller = ArtistSerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'seller', 'category', 'image', 'short_desc', 'price')


class ProductCreateSerializer(serializers.ModelSerializer):
    """Сериализация создание продукта"""
    title = serializers.CharField(max_length=100, required=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'image', 'short_desc', 'price', 'quantity')

    def create(self, validated_data):
        artist = Product.objects.update_or_create(**validated_data)
        return artist
