from django.urls import path
from . import views

urlpatterns = [
    path('categories/<int:pk>/', views.CategoryProductListView.as_view(), name='category'),
    path('artist-products/', views.ArtistProductView.as_view(), name='artist-products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('categories/', views.CategoryListView.as_view(), name='categories')
]