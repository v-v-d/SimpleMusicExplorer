from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from authapp.serializers import UserSerializer
from orderapp.models import OrderItem
from orderapp.serializers import OrderItemSerializer, OrderSerializer


class IsArtistOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        return obj.ordering.artist.user == request.user


class OrderMerchView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def get(self, request, pk):
        order_merch = OrderItem.objects.filter(order__artist_id=pk,
                                               type_product='m',
                                               order__payment_state='P')
        serializer = OrderItemSerializer(order_merch, many=True)

        return Response(serializer.data)


class OrderMusicView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def get(self, request, pk):
        order_music = OrderItem.objects.filter(order__artist_id=pk,
                                               type_product='t',
                                               order__payment_state='P')
        serializer = OrderItemSerializer(order_music, many=True)

        return Response(serializer.data)


