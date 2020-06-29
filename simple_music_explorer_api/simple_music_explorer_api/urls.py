"""simple_music_explorer_api URL Configuration"""




from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authapp.urls')),
    path('api/v1/merch/', include('merchapp.urls')),
]

