from django.http import HttpRequest

from scopes.authentication.ephemeral import is_ephemeral_user
from scopes.authentication.internal import is_internal_user
from scopes.permissions.base import PolyaxonPermission


class ScopesPermission(PolyaxonPermission):
    """
    Scopes based Permissions, depends on the authentication backend.
    """
    ENTITY = None
    SCOPE_MAPPING = None

    @staticmethod
    def _check_internal_or_ephemeral(request: HttpRequest) -> bool:
        return any([is_ephemeral_user(request.user), is_internal_user(request.user)])

    @staticmethod
    def _check_staff_or_superuser(request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_permission(self, request, view):
        if not request.auth:
            if not request.user.is_authenticated:
                return False
            # Session users are granted total access
            return True

        # (if that type of auth is allowed, then we should not check he scope)
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        if request.user.is_authenticated and self._check_staff_or_superuser(request=request):
            return True

        allowed_scopes = set(self.SCOPE_MAPPING.get(request.method, []))
        if not allowed_scopes:
            return True

        current_scopes = request.auth.scopes
        return any(s in allowed_scopes for s in current_scopes)
