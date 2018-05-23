from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from db.models.clusters import Cluster
from libs.views import ListCreateAPIView
from db.models.nodes import ClusterNode, NodeGPU
from runner.nodes.serializers import (
    ClusterNodeDetailSerializer,
    ClusterNodeSerializer,
    GPUSerializer
)


class ClusterNodeListView(ListCreateAPIView):
    queryset = ClusterNode.objects.filter(is_current=True)
    serializer_class = ClusterNodeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster=Cluster.load())


class ClusterNodeDetailView(RetrieveUpdateDestroyAPIView):
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
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.get_cluster_node())


class ClusterNodeGPUDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeGPUViewMixin):
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'index'
