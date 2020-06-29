from django.urls import path

from albumapp import views

urlpatterns = [
    path('', views.AlbumListView.as_view()),
    path('<int:artist_id>', views.AlbumListView.as_view()),
    path('<int:pk>', views.AlbumDetailView.as_view()),
    path('<int:pk>/tracks', views.TrackListView.as_view())
]
