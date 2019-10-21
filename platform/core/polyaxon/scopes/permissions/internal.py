from hestia.internal_services import InternalServices
from rest_framework import permissions

from django.http import HttpRequest
from django.views import View

from scopes.authentication.internal import is_authenticated_internal_user
from scopes.permissions.base import PolyaxonPermission


class IsInternal(PolyaxonPermission):
    """Custom permission to only allow internal clients."""

    SERVICE = None

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        check = (request.user and
                 not request.user.is_anonymous and
                 is_authenticated_internal_user(request.user))
        if not check:
            return False
        if self.SERVICE and request.user.service != self.SERVICE:
            return False
        return True

    def has_object_permission(self, request: HttpRequest, view: View, obj) -> bool:
        return True


class IsDockerizer(IsInternal):
    """Custom permission to only allow internal dockerizer client."""

    SERVICE = InternalServices.DOCKERIZER


class IsInitializer(IsInternal):
    """Custom permission to only allow internal initializer client."""

    SERVICE = InternalServices.INITIALIZER


class IsSidecar(IsInternal):
    """Custom permission to only allow internal sidecar client."""

    SERVICE = InternalServices.SIDECAR


class IsHelper(IsInternal):
    """Custom permission to only allow internal helper client."""
    SERVICE = InternalServices.HELPER


class IsRunner(IsInternal):
    """Custom permission to only allow internal runner client."""
    SERVICE = InternalServices.RUNNER


class IsAuthenticatedOrInternal(permissions.IsAuthenticated):
    """Custom permission to only allow internal clients."""

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        if super(IsAuthenticatedOrInternal, self).has_permission(request=request, view=view):
            return True
        return (request.user and
                not request.user.is_anonymous and
                is_authenticated_internal_user(request.user))

    def has_object_permission(self, request: HttpRequest, view: View, obj) -> bool:
        return True
