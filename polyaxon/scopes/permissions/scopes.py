from rest_framework import permissions

from scopes.authentication.ephemeral import is_ephemeral_user
from scopes.authentication.internal import is_internal_user


class ScopedPermission(permissions.BasePermission):
    """
    Scopes based Permissions, depends on the authentication backend.
    """
    SCOPE_MAPPING = {
        'HEAD': (),
        'GET': (),
        'POST': (),
        'PUT': (),
        'PATCH': (),
        'DELETE': (),
    }

    def has_permission(self, request, view):
        if not request.auth:
            if not request.user.is_authenticated():
                return False
            # If it's internal or ephemeral, we delegate to the next permission if there's any
            if any([is_ephemeral_user(request.user), is_internal_user(request.user)]):
                return False
            # Session users are granted total access
            return True

        allowed_scopes = set(self.SCOPE_MAPPING.get(request.method, []))
        current_scopes = request.auth.get_scopes()
        return any(s in allowed_scopes for s in current_scopes)

    def has_object_permission(self, request, view, obj):
        return False
