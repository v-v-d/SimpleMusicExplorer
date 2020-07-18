from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from musicapp.permissions import IsOwnerOrReadOnly
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCreateSerializer, CategoryListViewSerializer


# Create your views here.

class CategoryListView(APIView):
    """
    list all categories
    """
    # permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = CategoryListViewSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryProductListView(APIView):
    """
    Продукты определенной категории
    """
    # permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        products = Product.objects.filter(category__id=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ArtistProductView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(artist__user=request.user)
        serializer =ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serialize = ProductCreateSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product_update = Product.objects.filter(id=pk)
        serialize = ProductCreateSerializer(data=request.data)
        if serialize.is_valid():
            product_update.update(**serialize.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product_delete = Product.objects.filter(id=pk)
        product_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)