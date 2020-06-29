from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from AlbumsBackend import views

urlpatterns = [
    path('albums/', views.AlbumListView.as_view()),
    path('albums/<int:pk>', views.AlbumDetailView.as_view()),
    path('albums/<int:pk>/tracks', views.TrackListView.as_view())
]

# urlpatterns = format_suffix_patterns(urlpatterns)
