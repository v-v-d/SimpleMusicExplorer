import os
from django.urls import path
from . import views

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product')
]