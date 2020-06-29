from django.urls import path

from albumapp import views

urlpatterns = [
    path('', views.AlbumsListView.as_view()),
    path('artist/<int:artist_id>', views.AlbumListView.as_view()),
    path('artist/<int:artist_id>/<int:pk>', views.AlbumDetailView.as_view()),
    path('artist/<int:artist_id>/<int:pk>/tracks', views.TrackListView.as_view()),
    path('upload_cover', views.FileUploadView.as_view())
]