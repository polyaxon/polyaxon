from typing import Any

from rest_framework import permissions

from django.http import HttpRequest
from django.views import View


class PolyaxonPermission(permissions.BasePermission):
    """
    Polyaxon Base permission system.
    """

    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool:
        return False
