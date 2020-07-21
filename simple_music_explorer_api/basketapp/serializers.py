from rest_framework import serializers

from basketapp.models import BasketModel


class BasketSerializer(serializers.ModelSerializer):
    """
    A default class that can be used to represent the current user.
    In order to use this, the 'request' must have been provided as part of the context dictionary
    when instantiating the serializer.
    """
    owner = serializers.CurrentUserDefault()

    class Meta:
        model = BasketModel
        fields = ('id', 'owner', 'album', 'merch', 'type_product', 'price', 'quantity')


class BasketCreateSerializer(serializers.ModelSerializer):
    """Сериализация создание корзины"""

    class Meta:
        model = BasketModel
        fields = ('album', 'merch', 'price', 'quantity')

    def create(self, validated_data):
        basket, _ = BasketModel.objects.update_or_create(**validated_data)
        return basket