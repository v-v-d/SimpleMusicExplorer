from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from albumapp.models import AlbumModel, TrackModel
from albumapp.permissions import IsOwnerOrReadOnly
from albumapp.serializers import AlbumSerializer, TrackSerializer


class AlbumListView(APIView):
    """
    list all albums, or create a new one
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, artist_id=None):
        if artist_id:
            albums = AlbumModel.objects.filter(artist=artist_id).first()
        else:
            albums = AlbumModel.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(APIView):
    """
    retrieve, update or delete an album
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        album = get_object_or_404(AlbumModel, id=pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrackListView(APIView):
    """
    lists and add tracks on specific album
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        tracks = TrackModel.objects.filter(album_id=pk).all()
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = TrackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
