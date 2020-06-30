from django.urls import path

from musicapp import views

urlpatterns = [
    path('', views.AlbumsListView.as_view()),
    path('<int:pk>', views.AlbumDetailView.as_view()),
    path('<int:pk>/tracks', views.TrackListView.as_view()),

    path('artists/', views.ArtistListView.as_view()),
    path('artist/', views.ArtistView.as_view()),
    path('artist/<int:pk>/', views.ArtistDetail.as_view()),

    path('artist/<int:pk>/albums', views.AlbumListView.as_view()),
    path('upload_cover', views.FileUploadView.as_view())
]
