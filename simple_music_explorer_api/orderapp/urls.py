from django.urls import path

from orderapp.views import AddressView, OrderCreateView, OrderUpdateView

urlpatterns = [
    path('address/', AddressView.as_view()),
    path('create/', OrderCreateView.as_view()),
    path('update/', OrderUpdateView.as_view())
]
