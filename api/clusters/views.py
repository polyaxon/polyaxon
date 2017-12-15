# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated

from libs.views import ListCreateAPIView
from clusters.models import Cluster, ClusterNode, NodeGPU
from clusters.serializers import (
    ClusterSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
    GPUSerializer)


class ClusterDetailView(RetrieveAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Cluster.load()


class ClusterNodeListView(ListCreateAPIView):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(cluster=Cluster.load())


class ClusterNodeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ClusterNodeGPUViewMixin(object):
    def get_cluster_node(self):
        node_uuid = self.kwargs['node_uuid']
        return get_object_or_404(ClusterNode, uuid=node_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster_node=self.get_cluster_node())


class ClusterNodeGPUListView(ListCreateAPIView, ClusterNodeGPUViewMixin):
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.get_cluster_node())


class ClusterNodeGPUDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeGPUViewMixin):
    queryset = NodeGPU.objects.all()
    serializer_class = GPUSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
