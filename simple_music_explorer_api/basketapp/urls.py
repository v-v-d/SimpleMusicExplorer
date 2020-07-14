from django.urls import path

from .views import *

urlpatterns = [
    path('', BasketViewSet),
    path('change-basket/<int:pk>/', BasketChangeItem.as_view()),
]

