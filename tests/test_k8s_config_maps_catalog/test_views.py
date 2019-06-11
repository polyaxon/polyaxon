import pytest

from rest_framework import status

from api.k8s_config_maps.serializers import K8SConfigMapSerializer
from constants.urls import API_V1
from db.models.clusters import Cluster
from db.models.config_maps import K8SConfigMap
from factories.factory_k8s_config_maps import K8SConfigMapFactory
from tests.base.clients import AuthorizedClient
from tests.base.views import BaseViewTest


@pytest.mark.config_maps_catalog_mark
class TestK8SConfigMapListViewV1(BaseViewTest):
    serializer_class = K8SConfigMapSerializer
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory
    num_objects = 3
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.normal_client = AuthorizedClient()
        self.url = '/{}/catalogs/k8s_config_maps/'.format(API_V1)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        for i in data:
            assert i in self.serializer_class(self.queryset, many=True).data

        # Non admin
        resp = self.normal_client.get(self.url)
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
            'name': 'new_config',
            'description': 'some description',
            'config_map_ref': 'k8s_config1',
            'keys': ['key1', 'key2'],
            'tags': ['foo', 'bar']
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.owner.owner == Cluster.load()
        assert last_object.name == data['name']
        assert last_object.description == data['description']
        assert last_object.config_map_ref == data['config_map_ref']
        assert last_object.keys == data['keys']
        assert last_object.tags == data['tags']

        # Non admin
        data = {}
        resp = self.normal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        data = {
            'name': 'new_config',
            'description': 'some description',
            'config_map_ref': 'k8s_config1',
            'keys': ['key1', 'key2'],
            'tags': ['foo', 'bar']
        }
        resp = self.normal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.config_maps_catalog_mark
class TestK8SConfigMapDetailViewV1(BaseViewTest):
    serializer_class = K8SConfigMapSerializer
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.normal_client = AuthorizedClient()
        self.object = self.factory_class()
        self.url = '/{}/catalogs/k8s_config_maps/{}/'.format(API_V1, self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

        # Non admin can get
        resp = self.normal_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {
            'name': 'foo',
            'description': 'new description',
            'tags': ['foo', 'bar'],
            'config_map_ref': 'new_ref',
            'keys': ['key1', 'key2'],
        }
        assert self.object.name != data['name']
        assert self.object.description != data['description']
        assert self.object.tags != data['tags']
        assert self.object.config_map_ref != data['config_map_ref']
        assert self.object.keys != data['keys']

        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']
        assert new_object.description == data['description']
        assert new_object.tags == data['tags']
        assert new_object.config_map_ref == data['config_map_ref']
        assert new_object.keys == data['keys']

        # Non admin
        resp = self.normal_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_delete(self):
        # Non admin
        resp = self.normal_client.delete(self.url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0
