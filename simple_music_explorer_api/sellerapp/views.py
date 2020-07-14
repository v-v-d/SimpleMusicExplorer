from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from orderapp.models import OrderItem
from orderapp.serializers import OrderItemSerializer


class IsArtistOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        return obj.artist.user == request.user


class OrderMerchView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def get(self, request, pk):
        order_merch = OrderItem.objects.filter(artist__id=pk, album_product=None)
        serializer = OrderItemSerializer(order_merch, many=True)
        return Response(serializer.data)


class OrderMusicView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsArtistOwnerOrReadOnly]

    def get(self, request, pk):
        order_music = OrderItem.objects.filter(artist__id=pk, merch_product=None)
        serializer = OrderItemSerializer(order_music, many=True)
        return Response(serializer.data)


