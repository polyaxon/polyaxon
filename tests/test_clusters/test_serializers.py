# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from clusters.models import Cluster, NodeGPU, ClusterNode
from clusters.serializers import (
    ClusterSerializer,
    GPUSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
)

from factories.factory_clusters import GPUFactory, ClusterNodeFactory
from tests.utils import BaseTest


class TestGPUSerializer(BaseTest):
    serializer_class = GPUSerializer
    model_class = NodeGPU
    factory_class = GPUFactory
    expected_keys = {'uuid', 'cluster_node', 'serial', 'name', 'device', 'memory', 'updated_at',
                     'created_at', }

    def setUp(self):
        super().setUp()
        node = ClusterNodeFactory(cluster=Cluster.load())
        self.obj1 = self.factory_class(cluster_node=node)
        self.obj2 = self.factory_class(cluster_node=node)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('cluster_node') == self.obj1.cluster_node.uuid.hex
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestClusterNodeSerializer(BaseTest):
    serializer_class = ClusterNodeSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    expected_keys = {'uuid', 'name', 'hostname', 'role', 'memory', 'n_cpus', 'n_gpus', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class(cluster=Cluster.load())
        self.obj2 = self.factory_class(cluster=Cluster.load())

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestClusterNodeDetailsSerializer(BaseTest):
    serializer_class = ClusterNodeDetailSerializer
    model_class = ClusterNode
    expected_keys = {'uuid', 'name', 'cluster', 'hostname', 'role', 'docker_version',
                     'kubelet_version', 'os_image', 'kernel_version',
                     'schedulable_taints', 'schedulable_state', 'is_current',
                     'memory', 'n_cpus', 'n_gpus', 'status', 'gpus'}

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        self.obj1 = ClusterNodeFactory(cluster=self.cluster)
        self.obj2 = ClusterNodeFactory(cluster=self.cluster)
        self.gpu_obj1 = GPUFactory(cluster_node=self.obj1)
        self.gpu_obj2 = GPUFactory(cluster_node=self.obj2)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('cluster') == self.obj1.cluster.id
        assert len(data.pop('gpus')) == 1

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestClusterDetailSerializer(BaseTest):
    serializer_class = ClusterSerializer
    model_class = Cluster
    expected_keys = {'version_api', 'created_at', 'updated_at', 'nodes', }

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        ClusterNodeFactory(cluster=self.cluster)
        ClusterNodeFactory(cluster=self.cluster)

    def test_serialize_one(self):
        data = self.serializer_class(self.cluster).data

        assert set(data.keys()) == self.expected_keys
        assert len(data.pop('nodes')) == 2
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.cluster, k) == v
