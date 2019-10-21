import pytest

from rest_framework import status

from api.git_access.serializers import GitAccessSerializer
from constants.urls import API_V1
from db.models.clusters import Cluster
from db.models.git_access import GitAccess
from factories.factory_git_access import GitAccessFactory
from factories.factory_k8s_secrets import K8SSecretFactory
from tests.base.clients import AuthorizedClient
from tests.base.views import BaseViewTest


@pytest.mark.git_access_mark
class TestGitAccessListViewV1(BaseViewTest):
    serializer_class = GitAccessSerializer
    model_class = GitAccess
    factory_class = GitAccessFactory
    num_objects = 3
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.normal_client = AuthorizedClient()
        self.url = '/{}/catalogs/git_access/'.format(API_V1)
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

        secret = K8SSecretFactory()

        data = {
            'name': 'foo',
            'description': 'new description',
            'tags': ['foo', 'bar'],
            'host': 'https://foo.bar',
            'k8s_secret': secret.id,
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.owner.owner == Cluster.load()
        assert last_object.name == data['name']
        assert last_object.description == data['description']
        assert last_object.tags == data['tags']
        assert last_object.host == data['host']
        assert last_object.k8s_secret.id == data['k8s_secret']

        # Non admin
        data = {}
        resp = self.normal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

        data = {
            'name': 'foo',
            'description': 'new description',
            'tags': ['foo', 'bar'],
            'host': 'https://foo.bar',
            'k8s_secret': secret.id,
        }
        resp = self.normal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.git_access_mark
class TestGitAccessDetailViewV1(BaseViewTest):
    serializer_class = GitAccessSerializer
    model_class = GitAccess
    factory_class = GitAccessFactory
    HAS_AUTH = True
    ADMIN_USER = True

    def setUp(self):
        super().setUp()
        self.normal_client = AuthorizedClient()
        self.object = self.factory_class()
        self.url = '/{}/catalogs/git_access/{}/'.format(API_V1, self.object.name)
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
        secret = K8SSecretFactory()

        data = {
            'name': 'foo',
            'description': 'new description',
            'tags': ['foo', 'bar'],
            'host': 'https://foo.bar',
            'k8s_secret': secret.id,
        }
        assert self.object.name != data['name']
        assert self.object.description != data['description']
        assert self.object.tags != data['tags']
        assert self.object.host != data['host']
        assert self.object.k8s_secret != data['k8s_secret']

        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']
        assert new_object.description == data['description']
        assert set(new_object.tags) == set(data['tags'])
        assert new_object.host == data['host']
        assert new_object.k8s_secret.id == data['k8s_secret']

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
