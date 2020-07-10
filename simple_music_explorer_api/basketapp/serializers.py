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
        fields = ['owner', 'subtotal', 'total', 'basket_items']
