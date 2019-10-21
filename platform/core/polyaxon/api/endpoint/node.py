from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

import access

from access.resources import Resources
from api.endpoint.base import BaseEndpoint
from db.models.nodes import ClusterNode
from scopes.permissions.scopes import ScopesPermission


class NodePermission(ScopesPermission):
    SCOPE_MAPPING = access.get_scope_mapping_for(Resources.NODE)

    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        # This means that we allowed this auth backend on this endpoint
        if self._check_internal_or_ephemeral(request=request):
            return True

        return access.has_object_permission(
            resource=Resources.NODE,
            permission=NodePermission,
            request=request,
            view=view,
            obj=obj)


class NodeListEndpoint(BaseEndpoint):
    queryset = ClusterNode.objects.order_by('sequence').filter(is_current=True)
    permission_classes = (NodePermission,)
    AUDITOR_EVENT_TYPES = None


class NodeEndpoint(NodeListEndpoint):
    CONTEXT_KEYS = ('sequence',)
    CONTEXT_OBJECTS = ('node',)
    lookup_field = 'sequence'
    lookup_url_kwarg = 'sequence'

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.node = self.get_object()


class NodeResourceEndpoint(NodeListEndpoint):
    CONTEXT_KEYS = ('sequence',)
    CONTEXT_OBJECTS = ('node',)

    def enrich_queryset(self, queryset):
        return queryset.filter(cluster_node=self.node)

    def _initialize_context(self) -> None:
        #  pylint:disable=attribute-defined-outside-init
        super()._initialize_context()
        self.node = get_object_or_404(ClusterNode,
                                      sequence=self.sequence)
