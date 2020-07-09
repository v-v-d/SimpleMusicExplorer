from django.urls import path, include

from .views import url_redirect_404

urlpatterns = [
    path('users/set_username/', url_redirect_404),

    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
