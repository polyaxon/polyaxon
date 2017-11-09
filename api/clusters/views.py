# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
)

from libs.views import ListCreateAPIView
from clusters.models import Cluster, ClusterNode, GPU
from clusters.serializers import (
    ClusterSerializer,
    ClusterDetailSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
    GPUSerializer)


class ClusterListView(ListCreateAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)


class ClusterDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterDetailSerializer
    lookup_field = 'uuid'


class ClusterNodeViewMixin(object):
    def get_cluster(self):
        cluster_uuid = self.kwargs['cluster_uuid']
        return get_object_or_404(Cluster, uuid=cluster_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster=self.get_cluster())


class ClusterNodeListView(ListCreateAPIView, ClusterNodeViewMixin):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeSerializer

    def perform_create(self, serializer):
        serializer.save(cluster=self.get_cluster())


class ClusterNodeDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeViewMixin):
    queryset = ClusterNode.objects.all()
    serializer_class = ClusterNodeDetailSerializer
    lookup_field = 'uuid'


class ClusterNodeGPUViewMixin(object):
    def get_cluster_node(self):
        cluster_uuid = self.kwargs['cluster_uuid']
        cluster_node_uuid = self.kwargs['cluster_node_uuid']
        return get_object_or_404(ClusterNode, uuid=cluster_node_uuid, cluster__uuid=cluster_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(cluster_node=self.get_cluster_node())


class ClusterNodeGPUListView(ListCreateAPIView, ClusterNodeGPUViewMixin):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

    def perform_create(self, serializer):
        serializer.save(cluster_node=self.get_cluster_node())


class ClusterNodeGPUDetailView(RetrieveUpdateDestroyAPIView, ClusterNodeGPUViewMixin):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer
    lookup_field = 'uuid'
