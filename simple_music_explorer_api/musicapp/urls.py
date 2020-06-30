from django.urls import path

from musicapp import views

urlpatterns = [
    path('albums/all', views.AlbumsListView.as_view(), name='albums'),
    path('albums/<int:pk>', views.AlbumDetailView.as_view(), name='album'),
    path('albums/<int:pk>/tracks', views.TrackListView.as_view(), name='tracks'),

    path('artists', views.ArtistListView.as_view(), name='artists_all'),
    path('artists/<int:pk>/', views.ArtistDetail.as_view(), name='artist_detail'),
    path('artists/<int:pk>/albums', views.AlbumListView.as_view(), name='artist_albums'),

    path('upload_cover', views.FileUploadView.as_view(), name='upload_cover')
]
