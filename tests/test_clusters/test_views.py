import pytest

from rest_framework import status

from api.clusters.serializers import ClusterSerializer
from api.nodes.serializers import ClusterNodeDetailSerializer, ClusterNodeSerializer, GPUSerializer
from constants.nodes import NodeRoles
from db.models.clusters import Cluster
from db.models.nodes import ClusterNode, NodeGPU
from factories.factory_clusters import ClusterNodeFactory, GPUFactory, get_cluster_node
from polyaxon.urls import API_V1
from tests.utils import BaseViewTest


@pytest.mark.clusters_mark
class TestClusterDetailViewV1(BaseViewTest):
    serializer_class = ClusterSerializer
    model_class = Cluster
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.object = Cluster.load()
        self.url = '/{}/cluster/'.format(API_V1)

        # Create related fields
        for _ in range(2):
            ClusterNodeFactory(cluster=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['nodes']) == 2
        assert resp.data['nodes'] == ClusterNodeSerializer(self.object.nodes.all(), many=True).data


@pytest.mark.clusters_mark
class TestClusterNodeListViewV1(BaseViewTest):
    serializer_class = ClusterNodeSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    num_objects = 3
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        self.url = '/{}/cluster/nodes/'.format(API_V1)
        self.objects = [self.factory_class(cluster=self.cluster) for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter(cluster=self.cluster)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        for i in data:
            assert i in self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        query_data = self.serializer_class(self.queryset, many=True).data
        for i in data:
            assert i in query_data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        for i in data:
            assert i in query_data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            'name': 'new node',
            'role': NodeRoles.MASTER,
            'kubelet_version': 'v1.7.5',
            'os_image': 'Buildroot 2017.02',
            'kernel_version': '4.9.13',
            'memory': 100,
            'cpu': 2,
            'n_gpus': 0,
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.cluster == self.cluster
        assert last_object.memory == 100
        assert last_object.cpu == 2
        assert last_object.n_gpus == 0


@pytest.mark.clusters_mark
class TestClusterNodeDetailViewV1(BaseViewTest):
    serializer_class = ClusterNodeDetailSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.cluster = Cluster.load()
        self.object = self.factory_class(cluster=self.cluster)
        self.url = '/{}/nodes/{}/'.format(API_V1, self.object.sequence)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for _ in range(2):
            GPUFactory(cluster_node=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['gpus']) == 2
        assert resp.data['gpus'] == GPUSerializer(self.object.gpus.all(), many=True).data

    def test_patch(self):
        data = {
            'cpu': self.object.cpu + 1
        }
        assert self.object.cpu != data['cpu']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.cluster == self.object.cluster
        assert new_object.cpu != self.object.cpu
        assert new_object.cpu == data['cpu']
        assert new_object.gpus.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert NodeGPU.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert NodeGPU.objects.count() == 0


@pytest.mark.clusters_mark
class TestClusterNodeGPUListViewV1(BaseViewTest):
    serializer_class = GPUSerializer
    model_class = NodeGPU
    factory_class = GPUFactory
    num_objects = 3
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.cluster_node = ClusterNodeFactory(cluster=Cluster.load())
        self.url = '/{}/nodes/{}/gpus'.format(API_V1, self.cluster_node.sequence)
        self.objects = [self.factory_class(cluster_node=self.cluster_node)
                        for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            'serial': 'serial',
            'name': 'gpu',
            'memory': 100,
            'index': 1000
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.cluster_node == self.cluster_node
        assert last_object.serial == data['serial']
        assert last_object.name == data['name']
        assert last_object.memory == data['memory']
        assert last_object.index == data['index']


@pytest.mark.clusters_mark
class TestClusterNodeGPUDetailViewV1(BaseViewTest):
    serializer_class = GPUSerializer
    model_class = NodeGPU
    factory_class = GPUFactory
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(cluster_node=get_cluster_node())
        self.cluster_node = self.object.cluster_node
        self.url = '/{}/nodes/{}/gpus/{}'.format(API_V1,
                                                 self.cluster_node.sequence,
                                                 self.object.index)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {
            'serial': 'new_serial'
        }
        assert self.object.serial != data['serial']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.cluster_node == self.object.cluster_node
        assert new_object.serial != self.object.serial
        assert new_object.serial == data['serial']

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert ClusterNode.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
        assert ClusterNode.objects.count() == 1
