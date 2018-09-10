from rest_framework import permissions

from libs.authentication.ephemeral import is_internal_user


class IsEphemeral(permissions.BasePermission):
    """Custom permission to only allow ephemeral clients."""

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and is_internal_user(request.user):
            return True
        return False
