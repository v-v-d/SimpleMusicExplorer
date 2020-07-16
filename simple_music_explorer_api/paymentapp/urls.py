from django.urls import path

from .views import PaymentView, PaymentDoneView, PaymentCancelView

urlpatterns = [
    path('', PaymentView.as_view()),
    path('done/', PaymentDoneView.as_view()),
    path('cancel/', PaymentCancelView.as_view()),
]
