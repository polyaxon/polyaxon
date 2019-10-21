from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from db.models.activitylogs import ActivityLog
from scopes.permissions.scopes import ScopesPermission


class ActivityLogPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.ACTIVITY_LOG)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            resource=Resources.ACTIVITY_LOG,
            permission=ActivityLogPermission,
            request=request,
            view=view,
            obj=obj)


class ActivityLogEndpoint(BaseEndpoint):
    queryset = ActivityLog.objects
    permission_classes = (ActivityLogPermission,)
    AUDITOR_EVENT_TYPES = None
