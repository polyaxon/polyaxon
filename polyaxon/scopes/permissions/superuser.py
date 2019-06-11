from typing import Any

from rest_framework import permissions

from django.http import HttpRequest
from django.views import View

from scopes.exceptions import SuperuserRequired
from scopes.permissions.base import PolyaxonPermission


class SuperuserPermission(PolyaxonPermission):
    ALLOW_READ = False

    @staticmethod
    def _check_staff_or_superuser(request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if not request.user.is_authenticated:
            raise SuperuserRequired
        if self._check_staff_or_superuser(request):
            return True
        if self.ALLOW_READ and request.method in permissions.SAFE_METHODS:
            return True
        raise SuperuserRequired

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        return True
