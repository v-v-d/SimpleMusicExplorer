"""simple_music_explorer_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('schema', get_schema_view(
        title='Simple Music Explorer API',
        description='Our lovely little API :3',
        version='0.0.3',
    ), name='openapi-schema'),
    path('apiauth/', include('rest_framework.urls')),

    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authapp.urls'), name='auth'),
    path('api/v1/', include('musicapp.urls'), name='music'),
    path('api/v1/merch/', include('merchapp.urls'), name='merch'),
    path('api/v1/basket/', include('basketapp.urls'), name='basket'),
    path('api/v1/order/', include('orderapp.urls'), name='order'),
    path('api/v1/seller/', include('sellerapp.urls'), name='seller'),
    path('api/v1/customer/', include('customerapp.urls'), name='customer'),
]
