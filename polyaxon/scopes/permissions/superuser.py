from typing import Any

from django.http import HttpRequest
from django.views import View

from scopes.exceptions import SuperuserRequired
from scopes.permissions.base import PolyaxonPermission


class SuperuserPermission(PolyaxonPermission):

    @staticmethod
    def _check_staff_or_superuser(request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if not request.user.is_authenticated or not self._check_staff_or_superuser(request):
            raise SuperuserRequired
        return True

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        return True
