# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

from polyaxon_k8s.utils import nodes
from rest_framework import status

from api.urls import API_V1
from clusters.models import Cluster, ClusterNode, GPU
from clusters.serializers import (
    ClusterSerializer,
    ClusterDetailSerializer,
    ClusterNodeSerializer,
    ClusterNodeDetailSerializer,
    GPUSerializer,
)
from tests.factories.factory_clusters import ClusterFactory, ClusterNodeFactory, GPUFactory
from tests.utils import BaseTest


class TestClusterListViewV1(BaseTest):
    serializer_class = ClusterSerializer
    model_class = Cluster
    factory_class = ClusterFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.url = '/{}/clusters/'.format(API_V1)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
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

        next = resp.data.get('next')
        assert next is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data['version_api'] = {
            'build_date': '{}'.format(str(datetime.datetime.now())),
            'compiler': 'gc',
            'git_commit': '17d7182a7ccbb167074be7a87f0a68bd00d58d93',
            'git_tree_state': 'clean',
            'git_version': 'v1.7.5',
            'go_version': 'go1.8.3',
            'major': '1',
            'minor': '7',
            'platform': 'linux/amd64'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1


class TestClusterDetailViewV1(BaseTest):
    serializer_class = ClusterDetailSerializer
    model_class = Cluster
    factory_class = ClusterFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.object = self.factory_class()
        self.url = '/{}/clusters/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            ClusterNodeFactory(cluster=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['nodes']) == 2
        assert resp.data['nodes'] == ClusterNodeSerializer(self.object.nodes.all(), many=True).data

    def test_patch(self):
        data = {
            'version_api': {
                'build_date': '{}'.format(str(datetime.datetime.now())),
                'compiler': 'gc',
                'git_commit': '17d7182a7ccbb167074be7a87f0a68bd00d58d98',
                'git_tree_state': 'clean',
                'git_version': 'v1.7.6',
                'go_version': 'go1.8.4',
                'major': '1',
                'minor': '7',
                'platform': 'linux/amd64'
            }
        }
        assert self.object.version_api != data['version_api']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.version_api != self.object.version_api
        assert new_object.version_api == data['version_api']
        assert new_object.nodes.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert ClusterNode.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert ClusterNode.objects.count() == 0


class TestClusterNodeListViewV1(BaseTest):
    serializer_class = ClusterNodeSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.cluster = ClusterFactory()
        self.url = '/{}/clusters/{}/nodes/'.format(API_V1, self.cluster.uuid.hex)
        self.objects = [self.factory_class(cluster=self.cluster) for _ in range(self.num_objects)]
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

        next = resp.data.get('next')
        assert next is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next)
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
            'role': nodes.NodeRoles.MASTER,
            'kubelet_version': 'v1.7.5',
            'os_image': 'Buildroot 2017.02',
            'kernel_version': '4.9.13',
            'memory': 100,
            'n_cpus': 2,
            'n_gpus': 0,
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.cluster == self.cluster
        assert last_object.memory == 100
        assert last_object.n_cpus == 2
        assert last_object.n_gpus == 0


class TestClusterNodeDetailViewV1(BaseTest):
    serializer_class = ClusterNodeDetailSerializer
    model_class = ClusterNode
    factory_class = ClusterNodeFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.cluster = ClusterFactory()
        self.object = self.factory_class(cluster=self.cluster)
        self.url = '/{}/clusters/{}/nodes/{}/'.format(API_V1,
                                                      self.cluster.uuid.hex,
                                                      self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

        # Create related fields
        for i in range(2):
            GPUFactory(cluster_node=self.object)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data
        assert len(resp.data['gpus']) == 2
        assert resp.data['gpus'] == GPUSerializer(self.object.gpus.all(), many=True).data

    def test_patch(self):
        data = {
            'n_cpus': self.object.n_cpus + 1
        }
        assert self.object.n_cpus != data['n_cpus']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.cluster == self.object.cluster
        assert new_object.n_cpus != self.object.n_cpus
        assert new_object.n_cpus == data['n_cpus']
        assert new_object.gpus.count() == 2

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        assert GPU.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert GPU.objects.count() == 0


class TestClusterNodeGPUListViewV1(BaseTest):
    serializer_class = GPUSerializer
    model_class = GPU
    factory_class = GPUFactory
    num_objects = 3
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.cluster_node = ClusterNodeFactory()
        self.url = '/{}/clusters/{}/nodes/{}/gpus'.format(API_V1,
                                                          self.cluster_node.cluster.uuid.hex,
                                                          self.cluster_node.uuid.hex)
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

        next = resp.data.get('next')
        assert next is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next)
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
            'device': '/dev/nvidia3',
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.cluster_node == self.cluster_node
        assert last_object.serial == data['serial']
        assert last_object.name == data['name']
        assert last_object.memory == data['memory']
        assert last_object.device == data['device']


class TestClusterNodeGPUDetailViewV1(BaseTest):
    serializer_class = GPUSerializer
    model_class = GPU
    factory_class = GPUFactory
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.object = self.factory_class()
        self.cluster_node = self.object.cluster_node
        self.url = '/{}/clusters/{}/nodes/{}/gpus/{}'.format(API_V1,
                                                             self.cluster_node.cluster.uuid.hex,
                                                             self.cluster_node.uuid.hex,
                                                             self.object.uuid.hex)
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
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 0
        assert ClusterNode.objects.count() == 1
