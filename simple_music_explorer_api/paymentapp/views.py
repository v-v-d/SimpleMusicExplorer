import base64

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from orderapp.models import Orders
from orderapp.serializers import OrderSerializer
from paymentapp.models import BillingInformation


def checkout_orders(order, token):
    serializers = OrderSerializer(order, many=True)
    headers = {
        "Content-Type": "application/json",
        "Authorization": 'Bearer' + token}
    url = 'https://api.sandbox.paypal.com/v2/checkout/orders'
    # тестовые данные
    data = {
        "intent": "CAPTURE",
        "application_context": {
            "return_url": settings.RETURN_URL,
            "cancel_url": settings.CANCEL_URL,
            "brand_name": "SimpleMusicExplorer",
            "landing_page": "BILLING",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "PAY_NOW"
        },
        "purchase_units": [
            {
                "soft_descriptor": "SimpleMusicExplorer",
                "amount": {
                    "currency_code": "USD",
                    "value": f"{order.total_sum}",

                },
                "items": serializers.data,
            }
        ]

    }
    result = requests.post(url, data, headers=headers)
    return result


def paypal_token(client_id, client_secret):

    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(
            base64.b64encode(
                (client_id + ":" + client_secret).encode()).decode())}

    token = requests.post(url, data, headers=headers)
    return token


class PaymentView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        order_id = request.data.get('order_id')
        order = get_object_or_404(Orders, id=order_id, owner=request.user, payment_state='NP')

        billing = BillingInformation(seller=order.artist)
        client_id = billing.client_id
        client_secret = billing.client_secret
        token = paypal_token(client_id, client_secret)

        respons = checkout_orders(order, token).json()
        return Response(respons)


class PaymentDoneView(APIView):
    """
        В этой вью будет меняться статус заказа на оплачено
    """
    pass


class PaymentCancelView(APIView):
    """
        В этой вью будет удаляться заказ и все его зависимости
    """
    pass
