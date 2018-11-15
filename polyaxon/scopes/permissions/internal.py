from rest_framework import permissions

from scopes.authentication.internal import is_authenticated_internal_user
from scopes.permissions.base import PolyaxonPermission


class IsInternal(PolyaxonPermission):
    """Custom permission to only allow internal clients."""

    def has_permission(self, request, view):
        return (request.user and
                not request.user.is_anonymous and
                is_authenticated_internal_user(request.user))


class IsAuthenticatedOrInternal(permissions.IsAuthenticated):
    """Custom permission to only allow internal clients."""

    def has_permission(self, request, view):
        if super(IsAuthenticatedOrInternal, self).has_permission(request=request, view=view):
            return True
        return (request.user and
                not request.user.is_anonymous and
                is_authenticated_internal_user(request.user))

    def has_object_permission(self, request, view, obj):
        return True
