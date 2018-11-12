from rest_framework.generics import get_object_or_404

import access
from access.entities import Entities

from api.endpoint.base import BaseEndpoint
from db.models.owner import Owner
from scopes.permissions.scopes import ScopesPermission


class OwnerPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('Owner')

    def has_object_permission(self, request, view, obj):
        return access.has_object_permission(
            entity=Entities.OWNER,
            permission=OwnerPermission,
            request=request,
            view=view,
            obj=obj)


class OwnerEndpoint(BaseEndpoint):
    queryset = Owner.objects
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    lookup_url_kwarg = 'owner_name'

    def _initialize_context(self):
        super()._initialize_context()
        self.owner = self.get_object()


class OwnerResourceEndpoint(BaseEndpoint):
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    lookup_url_kwarg = 'owner_name'

    def _initialize_context(self):
        super()._initialize_context()
        self.owner = get_object_or_404(Owner, name=self.owner_name)

    def _validate_context(self):
        super()._validate_context()
        OwnerPermission().has_object_permission(request=self.request,
                                                view=self,
                                                obj=self.owner)
