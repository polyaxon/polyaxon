from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from scopes.permissions.superuser import SuperuserPermission


class AdminPermission(SuperuserPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.ADMIN)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return access.has_object_permission(
            resource=Resources.ADMIN,
            permission=AdminPermission,
            request=request,
            view=view,
            obj=obj)


class AdminOrReadOnlyPermission(AdminPermission):
    ALLOW_READ = True

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        return access.has_object_permission(
            resource=Resources.ADMIN,
            permission=AdminOrReadOnlyPermission,
            request=request,
            view=view,
            obj=obj)


class AdminListEndpoint(BaseEndpoint):
    permission_classes = (AdminPermission,)
    AUDITOR_EVENT_TYPES = None


class AdminOrReadOnlyListEndpoint(BaseEndpoint):
    permission_classes = (AdminOrReadOnlyPermission,)
    AUDITOR_EVENT_TYPES = None


class AdminOrReadOnlyEndpoint(AdminOrReadOnlyListEndpoint):
    CONTEXT_KEYS = ('name',)
    CONTEXT_OBJECTS = ('entry',)
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.entry = self.get_object()
