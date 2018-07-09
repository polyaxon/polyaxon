from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.nodes.serializers import ClusterNodeDetailSerializer, ClusterNodeSerializer, GPUSerializer
from api.utils.views import ListCreateAPIView
from db.models.clusters import Cluster
from db.models.nodes import ClusterNode, NodeGPU


class ClusterNodeListView(ListCreateAPIView):
    """
    get:
        List cluster nodes.

    post:
        Create a cluster node.
    """
    queryset = ClusterNode.objects.order_by('sequence').filter(is_current=True)
    serializer_class = ClusterNodeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster=Cluster.load())


class ClusterNodeDetailView(RetrieveUpdateDestroyAPIView):
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
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'sequence'


class ClusterNodeGPUViewMixin(object):
    def get_cluster_node(self):
        sequence = self.kwargs['sequence']
        return get_object_or_404(ClusterNode, sequence=sequence)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster_node=self.get_cluster_node())


class ClusterNodeGPUListView(ListCreateAPIView, ClusterNodeGPUViewMixin):
    """
    get:
        List cluster node GPUs.

    post:
        Create a cluster node GPU.
    """
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.get_cluster_node())


class ClusterNodeGPUDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeGPUViewMixin):
    """
    get:
        Get a custer node GPU details.
    patch:
        Update a custer node GPU details.
    delete:
        Delete a custer node GPU.
    """
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'index'
