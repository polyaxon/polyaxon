from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from db.models.owner import Owner
from scopes.permissions.scopes import ScopesPermission


class AdminPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.ADMIN)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            resource=Resources.ADMIN,
            permission=AdminPermission,
            request=request,
            view=view,
            obj=obj)


class AdminProjectListPermission(AdminPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.ADMIN)


class AdminEndpoint(BaseEndpoint):
    queryset = Owner.objects
    permission_classes = (AdminPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    CONTEXT_OBJECTS = ('owner',)
    lookup_url_kwarg = 'owner_name'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.owner = self.get_object()


class AdminResourceEndpoint(BaseEndpoint):
    permission_classes = (AdminPermission,)
    AUDITOR_EVENT_TYPES = None
    CONTEXT_KEYS = ('owner_name',)
    CONTEXT_OBJECTS = ('owner',)
    lookup_url_kwarg = 'owner_name'

    def filter_queryset(self, queryset):
        queryset = queryset.filter(owner=self.owner)
        return super().filter_queryset(queryset=queryset)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.owner = get_object_or_404(Owner, name=self.owner_name)

    def _validate_context(self) -> None:
        super()._validate_context()
        permission = self.permission_classes[0]()
        if not permission.has_object_permission(request=self.request,
                                                view=self,
                                                obj=self.owner):
            self.permission_denied(
                self.request, message=getattr(permission, 'message', None)
            )
