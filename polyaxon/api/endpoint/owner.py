import access

from api.endpoint.base import BaseEndpoint
from scopes.permissions.scopes import ScopesPermission


class OwnerPermission(ScopesPermission):
    ENTITY = access.entites.OWNER
    SCOPE_MAPPING = access.get_scope_mapping_for('Owner')

    def has_object_permission(self, request, view, obj):
        return access.has_object_permission(
            entity=self.ENTITY,
            permission=self,
            request=request,
            view=view,
            obj=obj)


class OwnerEndpoint(BaseEndpoint):
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    lookup_url_kwarg = 'owner_name'

    def _initialize_context(self):
        self.request.owner = self.get_object()
