from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt

from .views import url_redirect_404

urlpatterns = [
    path('users/set_username/', url_redirect_404),  # блокировка url

    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    # path('', include('djoser.urls.jwt')),
]
# /users/
# /users/me/
# /users/confirm/
# /users/resend_activation/
# /users/set_password/
# /users/reset_password/
# /users/reset_password_confirm/
# /users/set_username/
# /users/reset_username/
# /users/reset_username_confirm/
# /token/login/ (Token Based Authentication)
# /token/logout/ (Token Based Authentication)
# /jwt/create/ (JSON Web Token Authentication)
# /jwt/refresh/ (JSON Web Token Authentication)
# /jwt/verify/ (JSON Web Token Authentication)