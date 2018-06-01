from rest_framework import permissions

from libs.permissions.authentication import is_internal_user


class IsInternal(permissions.BasePermission):
    """Custom permission to only allow internal clients."""

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and is_internal_user(request.user):
            return True
        return False


class IsAuthenticatedOrInternal(permissions.IsAuthenticated):
    """Custom permission to only allow internal clients."""

    def has_permission(self, request, view):
        if super(IsAuthenticatedOrInternal, self).has_permission(request=request, view=view):
            return True
        if request.user and not request.user.is_anonymous and is_internal_user(request.user):
            return True
        return False
