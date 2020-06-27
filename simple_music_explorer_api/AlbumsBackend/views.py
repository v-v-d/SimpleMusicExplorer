from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from AlbumsBackend.models import AlbumModel
from AlbumsBackend.serializers import AlbumSerializer


class AlbumListView(APIView):
    """
    list all albums, or create a new one
    """
    def get(self, request):
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
    def get_object(self, pk):
        try:
            return AlbumModel.objects.get(pk=pk)
        except AlbumModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SongListView(APIView):
    pass
