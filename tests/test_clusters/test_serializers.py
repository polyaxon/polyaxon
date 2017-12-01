# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.test import TestCase

from clusters.models import Cluster, GPU, ClusterNode
from clusters.serializers import (
    ClusterSerializer,
    GPUSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
    ClusterDetailSerializer,
)

from tests.factories.factory_clusters import ClusterFactory, GPUFactory, ClusterNodeFactory


class TestGPUSerializer(TestCase):
    serializer_class = GPUSerializer
    model_class = GPU
    factory_class = GPUFactory
    expected_keys = {'uuid', 'cluster_node', 'serial', 'name', 'device', 'memory', 'updated_at',
                     'created_at', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

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


class TestClusterNodeSerializer(TestCase):
    serializer_class = ClusterNodeSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    expected_keys = {'uuid', 'name', 'hostname', 'role', 'memory', 'n_cpus', 'n_gpus', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

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


class TestClusterNodeDetailsSerializer(TestCase):
    serializer_class = ClusterNodeDetailSerializer
    model_class = ClusterNode
    expected_keys = {'uuid', 'name', 'cluster', 'hostname', 'role', 'docker_version',
                     'kubelet_version', 'os_image', 'kernel_version',
                     'schedulable_taints', 'schedulable_state', 'is_current',
                     'memory', 'n_cpus', 'n_gpus', 'status', 'gpus'}

    def setUp(self):
        super().setUp()
        self.gpu_obj1 = GPUFactory()
        self.obj1 = self.gpu_obj1.cluster_node
        self.gpu_obj2 = GPUFactory()
        self.obj2 = self.gpu_obj2.cluster_node

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('cluster') == self.obj1.cluster.uuid.hex
        assert len(data.pop('gpus')) == 1

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestClusterSerializer(TestCase):
    serializer_class = ClusterSerializer
    model_class = Cluster
    factory_class = ClusterFactory
    expected_keys = {'uuid', 'user', 'version_api', 'created_at', 'updated_at', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestClusterDetailSerializer(TestCase):
    serializer_class = ClusterDetailSerializer
    model_class = Cluster
    expected_keys = {'uuid', 'user', 'version_api', 'created_at', 'updated_at', 'nodes', }

    def setUp(self):
        super().setUp()
        self.node_obj1 = ClusterNodeFactory()
        self.obj1 = self.node_obj1.cluster
        self.node_obj2 = ClusterNodeFactory()
        self.obj2 = self.node_obj2.cluster

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert len(data.pop('nodes')) == 1
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
