from django.urls import path

from orderapp.views import AddressView, NeedAnAddress, InvoiceForPaymentView

urlpatterns = [
    path('need-an-address/', NeedAnAddress.as_view()),
    path('address/', AddressView.as_view()),
    path('order-list/', InvoiceForPaymentView.as_view()),
]
