from typing import Any

from django.http import HttpRequest
from django.views import View

from scopes.authentication.ephemeral import is_authenticated_ephemeral_user
from scopes.permissions.base import PolyaxonPermission


class IsEphemeral(PolyaxonPermission):
    """Custom permission to only allow ephemeral clients."""

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return (request.user and
                not request.user.is_anonymous and
                is_authenticated_ephemeral_user(request.user))

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        return True
