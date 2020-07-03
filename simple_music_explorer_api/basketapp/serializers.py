from rest_framework import serializers

from basketapp.models import BasketModel


class BasketSerializer(serializers.ModelSerializer):
    owner = serializers.CurrentUserDefault()

    class Meta:
        model = BasketModel
        fields = ['owner', 'subtotal', 'total', 'basket_items']
