import os
from django.urls import path
from .views import ProductList

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('', ProductList.as_view(), name='all')
]