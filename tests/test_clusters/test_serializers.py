import pytest

from api.clusters.serializers import ClusterSerializer
from api.nodes.serializers import (
    ClusterNodeDetailSerializer,
    ClusterNodeSerializer,
    ClusterRunnerSerializer,
    GPUSerializer
)
from db.models.clusters import Cluster
from db.models.nodes import ClusterNode, NodeGPU
from factories.factory_clusters import ClusterNodeFactory, GPUFactory
from tests.utils import BaseTest


@pytest.mark.clusters
class TestGPUSerializer(BaseTest):
    serializer_class = GPUSerializer
    model_class = NodeGPU
    factory_class = GPUFactory
    expected_keys = {'uuid', 'cluster_node', 'serial', 'name', 'index', 'memory', 'updated_at',
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


@pytest.mark.clusters
class TestClusterNodeSerializer(BaseTest):
    serializer_class = ClusterNodeSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    expected_keys = {'uuid', 'sequence', 'name', 'hostname', 'role', 'memory', 'cpu', 'n_gpus', }

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


@pytest.mark.clusters
class TestClusterNodeDetailsSerializer(BaseTest):
    serializer_class = ClusterNodeDetailSerializer
    model_class = ClusterNode
    expected_keys = {'uuid', 'name', 'hostname', 'role', 'docker_version',
                     'kubelet_version', 'os_image', 'kernel_version',
                     'schedulable_taints', 'schedulable_state', 'is_current',
                     'memory', 'cpu', 'n_gpus', 'status', 'gpus', 'sequence'}

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
        assert len(data.pop('gpus')) == 1

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.clusters
class TestClusterDetailSerializer(BaseTest):
    serializer_class = ClusterSerializer
    model_class = Cluster
    expected_keys = {'uuid', 'version_api', 'created_at', 'updated_at', }

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        ClusterNodeFactory(cluster=self.cluster)
        ClusterNodeFactory(cluster=self.cluster)

    def test_serialize_one(self):
        data = self.serializer_class(self.cluster).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.cluster.uuid.hex
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.cluster, k) == v


@pytest.mark.clusters
class TestRunnerClusterDetailSerializer(BaseTest):
    serializer_class = ClusterRunnerSerializer
    model_class = Cluster
    expected_keys = {'uuid', 'version_api', 'created_at', 'updated_at', 'nodes', }

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        ClusterNodeFactory(cluster=self.cluster)
        ClusterNodeFactory(cluster=self.cluster)

    def test_serialize_one(self):
        data = self.serializer_class(self.cluster).data

        assert set(data.keys()) == self.expected_keys
        assert len(data.pop('nodes')) == 2
        assert data.pop('uuid') == self.cluster.uuid.hex
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.cluster, k) == v
