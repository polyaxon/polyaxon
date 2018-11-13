from rest_framework.generics import get_object_or_404

from api.endpoint.base import (
    CreateEndpoint,
    ListEndpoint,
    DestroyEndpoint,
    UpdateEndpoint,
    RetrieveEndpoint
)
from api.endpoint.node import NodeListEndpoint, NodeEndpoint, NodeResourceEndpoint
from api.nodes.serializers import ClusterNodeDetailSerializer, ClusterNodeSerializer, GPUSerializer
from db.models.clusters import Cluster
from db.models.nodes import ClusterNode, NodeGPU


class ClusterNodeListView(NodeListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List cluster nodes.

    post:
        Create a cluster node.
    """
    serializer_class = ClusterNodeSerializer

    def perform_create(self, serializer):
        serializer.save(cluster=Cluster.load())


class ClusterNodeDetailView(NodeEndpoint, RetrieveEndpoint, UpdateEndpoint, DestroyEndpoint):
    """
    get:
        Get a custer node details.
    patch:
        Update a custer node details.
    delete:
        Delete a custer node.
    """
    queryset = ClusterNode.objects.filter(is_current=True)
    serializer_class = ClusterNodeDetailSerializer


class ClusterNodeGPUViewMixin(object):
    def get_cluster_node(self):
        sequence = self.kwargs['sequence']
        return get_object_or_404(ClusterNode, sequence=sequence)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster_node=self.get_cluster_node())


class ClusterNodeGPUListView(NodeResourceEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List cluster node GPUs.

    post:
        Create a cluster node GPU.
    """
    queryset = NodeGPU.objects
    serializer_class = GPUSerializer

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.node)


class ClusterNodeGPUDetailView(NodeResourceEndpoint,
                               RetrieveEndpoint,
                               UpdateEndpoint,
                               DestroyEndpoint):
    """
    get:
        Get a custer node GPU details.
    patch:
        Update a custer node GPU details.
    delete:
        Delete a custer node GPU.
    """
    queryset = NodeGPU.objects
    serializer_class = GPUSerializer
    lookup_field = 'index'
    lookup_url_kwarg = 'index'
