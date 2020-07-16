from django.urls import path

from customerapp.views import OrderHistoryView, OwnerMusicCatalogView

urlpatterns = [
    path('orders-history/', OrderHistoryView.as_view()),
    path('owner-music-catalog/', OwnerMusicCatalogView.as_view())
]
