from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to use it.
    """

    def has_object_permission(self, request, view, obj):
        """
        checking whether the user is owner or not
        """
        return obj.owner.user == request.user
