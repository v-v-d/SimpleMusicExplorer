from django.urls import path

from orderapp.views import AddressView, InvoiceForPaymentView

urlpatterns = [
    path('address/', AddressView.as_view()),
    path('order-list/', InvoiceForPaymentView.as_view()),
]
