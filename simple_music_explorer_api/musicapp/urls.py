from django.urls import path

from musicapp import views

urlpatterns = [
    path('', views.AlbumsListView.as_view(), name='albums'),
    path('<int:pk>', views.AlbumDetailView.as_view(), name='album'),
    path('<int:pk>/tracks', views.TrackListView.as_view(), name='tracks'),

    path('artists/', views.ArtistListView.as_view(), name='artists'),
    path('artist/', views.ArtistView.as_view(), name='artist'),
    path('artist/<int:pk>/', views.ArtistDetail.as_view(), name='artist_detail'),

    path('artist/<int:pk>/albums', views.AlbumListView.as_view(), name='artist_albums'),
    path('upload_cover', views.FileUploadView.as_view(), name='upload_cover')
]
