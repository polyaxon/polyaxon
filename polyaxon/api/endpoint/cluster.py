import access

from access.entities import Entities
from api.endpoint.base import BaseEndpoint
from db.models.clusters import Cluster
from scopes.permissions.scopes import ScopesPermission


class ClusterPermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for('Cluster')

    def has_object_permission(self, request, view, obj):
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            entity=Entities.OWNER,
            permission=ClusterPermission,
            request=request,
            view=view,
            obj=obj)


class ClusterEndpoint(BaseEndpoint):
    queryset = Cluster.objects.all()
    permission_classes = (ClusterPermission,)
    AUDITOR_EVENT_TYPES = None
