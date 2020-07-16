import base64

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from orderapp.models import Orders
from paymentapp.models import BillingInformation


def checkout_orders(order, token):
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
            "brand_name": "EXAMPLE INC",
            "landing_page": "BILLING",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "CONTINUE"
        },
        "purchase_units": [
            {
                "reference_id": "PUHF",
                "description": "Sporting Goods",

                "custom_id": "CUST-HighFashions",
                "soft_descriptor": "HighFashions",
                "amount": {
                    "currency_code": "USD",
                    "value": "220.00",
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": "180.00"
                        },
                        "shipping": {
                            "currency_code": "USD",
                            "value": "20.00"
                        },
                        "handling": {
                            "currency_code": "USD",
                            "value": "10.00"
                        },
                        "tax_total": {
                            "currency_code": "USD",
                            "value": "20.00"
                        },
                        "shipping_discount": {
                            "currency_code": "USD",
                            "value": "10"
                        }
                    }
                },
                "items": [
                    {
                        "name": "T-Shirt",
                        "description": "Green XL",
                        "sku": "sku01",
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": "90.00"
                        },
                        "tax": {
                            "currency_code": "USD",
                            "value": "10.00"
                        },
                        "quantity": "1",
                        "category": "PHYSICAL_GOODS"
                    },
                    {
                        "name": "Shoes",
                        "description": "Running, Size 10.5",
                        "sku": "sku02",
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": "45.00"
                        },
                        "tax": {
                            "currency_code": "USD",
                            "value": "5.00"
                        },
                        "quantity": "2",
                        "category": "PHYSICAL_GOODS"
                    }
                ],
                "shipping": {
                    "method": "United States Postal Service",
                    "name": {
                        "full_name": "John Doe"
                    },
                    "address": {
                        "address_line_1": "123 Townsend St",
                        "address_line_2": "Floor 6",
                        "admin_area_2": "San Francisco",
                        "admin_area_1": "CA",
                        "postal_code": "94107",
                        "country_code": "US"
                    }
                }
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
        order_id = address_id = request.data.get('order_id')
        order = get_object_or_404(Orders, id=order_id)

        billing = BillingInformation(seller=order.artist)
        client_id = billing.client_id
        client_secret = billing.client_secret
        token = paypal_token(client_id, client_secret)

        respons = checkout_orders(order, token).json()
        return Response(respons)


class PaymentDoneView(APIView):
    pass


class PaymentCancelView(APIView):
    pass
