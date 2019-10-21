from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from db.models.clusters import Cluster
from scopes.permissions.scopes import ScopesPermission


class ClusterPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.CLUSTER)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            resource=Resources.CLUSTER,
            permission=ClusterPermission,
            request=request,
            view=view,
            obj=obj)


class ClusterEndpoint(BaseEndpoint):
    queryset = Cluster.objects.all()
    permission_classes = (ClusterPermission,)
    AUDITOR_EVENT_TYPES = None
