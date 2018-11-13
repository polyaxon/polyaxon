from rest_framework.generics import get_object_or_404

import access

from access.entities import Entities
from api.endpoint.base import BaseEndpoint
from db.models.owner import Owner
from scopes.permissions.scopes import ScopesPermission


class OwnerPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('Owner')

    def has_object_permission(self, request, view, obj):
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            entity=Entities.OWNER,
            permission=OwnerPermission,
            request=request,
            view=view,
            obj=obj)


class OwnerProjectListPermission(OwnerPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('OwnerProjectList')


class OwnerEndpoint(BaseEndpoint):
    queryset = Owner.objects
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    CONTEXT_OBJECTS = ('owner',)
    lookup_url_kwarg = 'owner_name'

    def _initialize_context(self):
        super()._initialize_context()
        self.owner = self.get_object()


class OwnerResourceEndpoint(BaseEndpoint):
    permission_classes = (OwnerPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    CONTEXT_OBJECTS = ('owner',)
    lookup_url_kwarg = 'owner_name'

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.owner)
        return super().filter_queryset(queryset=queryset)

    def _initialize_context(self):
        super()._initialize_context()
        self.owner = get_object_or_404(Owner, name=self.owner_name)

    def _validate_context(self):
        super()._validate_context()
        permission = self.permission_classes[0]()
        if not permission.has_object_permission(request=self.request,
                                                view=self,
                                                obj=self.owner):
            self.permission_denied(
                self.request, message=getattr(permission, 'message', None)
            )
