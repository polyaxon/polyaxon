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


class AdminEndpoint(BaseEndpoint):
    permission_classes = (AdminPermission,)
    AUDITOR_EVENT_TYPES = None
