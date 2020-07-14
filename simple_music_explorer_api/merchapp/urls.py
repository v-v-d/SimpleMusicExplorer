from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.CategoryProductListView.as_view()),
    path('artist-products/', views.ArtistProductView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view())
]