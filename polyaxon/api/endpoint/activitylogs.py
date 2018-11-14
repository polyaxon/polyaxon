import access

from access.entities import Entities
from api.endpoint.base import BaseEndpoint
from db.models.activitylogs import ActivityLog
from db.models.nodes import ClusterNode
from scopes.permissions.scopes import ScopesPermission


class ActivityLogPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('ActivityLog')

    def has_object_permission(self, request, view, obj):
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            entity=Entities.OWNER,
            permission=ActivityLogPermission,
            request=request,
            view=view,
            obj=obj)


class ActivityLogEndpoint(BaseEndpoint):
    queryset = ActivityLog.objects
    permission_classes = (ActivityLogPermission,)
    AUDITOR_EVENT_TYPES = None
