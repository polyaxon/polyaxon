import access

from api.endpoint.base import BaseEndpoint
from scopes.permissions.scopes import ScopesPermission


class OwnerPermission(ScopesPermission):
    ENTITY = 'Owner'
    SCOPE_MAPPING = access.get_scope_mapping_for('Owner')

    def has_object_permission(self, request, view, obj):
        return access.has_object_permission(
            entity=self.ENTITY,
            permission=self,
            request=request,
            view=view,
            obj=obj)


class ProjectEndpoint(BaseEndpoint):
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner',)
