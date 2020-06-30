from rest_framework import permissions

from musicapp.models import ArtistModel


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.artist.user == request.user

#
# class CustomerAccessPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         if request.method == 'GET':
#             return True
#
#         pk = request.parser_context['kwargs']['pk']
#         user = ArtistModel.objects.filter(id=pk).first()
#         if user and user.user_id == request.user.id and request.user.is_artist:
#             return True
#         return False
