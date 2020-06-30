from django.urls import path

from musicapp import views

urlpatterns = [
    path('album/all', views.AlbumsListView.as_view(), name='albums'),
    path('album/<int:pk>', views.AlbumDetailView.as_view(), name='album'),
    path('album/<int:pk>/tracks', views.TrackListView.as_view(), name='tracks'),

    path('all', views.ArtistListView.as_view(), name='artists'),
    path('', views.ArtistView.as_view(), name='artist'),
    path('<int:pk>/', views.ArtistDetail.as_view(), name='artist_detail'),
    path('<int:pk>/albums', views.AlbumListView.as_view(), name='artist_albums'),

    path('upload_cover', views.FileUploadView.as_view(), name='upload_cover')
]
