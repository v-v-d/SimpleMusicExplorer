from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer

# Create your views here.


class ProductListView(APIView):
    "output a list of products"

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    "output of product"

    def get(self, request, pk):
        product = Product.objects.get(id=pk, is_active=True)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
