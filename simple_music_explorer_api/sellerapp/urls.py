from django.urls import path, include

from .views import OrderMerchView, OrderMusicView

urlpatterns = [
    path('orders-merch/<int:pk>/', OrderMerchView.as_view()),
    path('orders-music/<int:pk>/', OrderMusicView.as_view())
]
