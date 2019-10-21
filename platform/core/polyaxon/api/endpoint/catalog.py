from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from scopes.permissions.scopes import ScopesPermission


class CatalogPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.CATALOG)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            resource=Resources.CATALOG,
            permission=CatalogPermission,
            request=request,
            view=view,
            obj=obj)


class CatalogListEndpoint(BaseEndpoint):
    queryset = None
    permission_classes = (CatalogPermission,)
    AUDITOR_EVENT_TYPES = None


class CatalogEntryEndpoint(CatalogListEndpoint):
    CONTEXT_KEYS = ('uuid',)
    CONTEXT_OBJECTS = ('entry',)
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.entry = self.get_object()
