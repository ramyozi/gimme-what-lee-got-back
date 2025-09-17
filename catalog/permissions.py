from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admins.
    Read-only for everyone else.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "admin"


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow users to update/delete their own objects.
    Admins can manage everything.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (obj.user == request.user or request.user.role == "admin")
        )
