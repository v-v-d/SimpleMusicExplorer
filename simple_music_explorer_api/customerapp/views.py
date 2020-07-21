from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from orderapp.models import OrderItem
from orderapp.serializers import OrderItemSerializer


class OrderHistoryView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        order_item = OrderItem.objects.filter(order__owner=request.user,
                                              order__payment_state='P')
        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data)


class OwnerMusicCatalogView(APIView):

    def get(self, request):
        order_item = OrderItem.objects.filter(order__owner=request.user,
                                              type_product='t',
                                              order__payment_state='P')
        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data)
