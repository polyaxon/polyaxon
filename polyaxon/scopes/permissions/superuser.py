from typing import Any

from django.http import HttpRequest
from django.views import View

from scopes.exceptions import SuperuserRequired
from scopes.permissions.base import PolyaxonPermission


class SuperuserPermission(PolyaxonPermission):
    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if request.user.is_authenticated and not request.user.is_superuser:
            raise SuperuserRequired
        return False

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        return True
