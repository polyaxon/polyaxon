# pylint:disable=too-many-lines

import pytest

from rest_framework import status

import conf

from api.options.serializers import ConfigOptionSerializer
from constants.urls import API_V1
from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from db.models.owner import Owner
from options.registry import node_selectors
from options.registry.node_selectors import NODE_SELECTORS_BUILD_JOBS, NODE_SELECTORS_JOBS
from tests.base.clients import AuthorizedClient
from tests.base.views import BaseViewTest


@pytest.mark.configs_mark
class TesClusterConfigOptionsViewV1(BaseViewTest):
    model_class = ConfigOption
    num_objects = 4
    HAS_AUTH = True
    ADMIN_USER = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.owner = self.get_owner()
        self.url = self.get_url()
        self.queryset = self.model_class.objects.filter(owner=self.owner)

    def get_owner(self):
        return Owner.objects.get(name=Cluster.load().uuid)

    def get_url(self):
        return '/{}/options/'.format(API_V1)

    def test_non_owner(self):
        new_client = AuthorizedClient()

        assert new_client.get(self.url + '?keys=value1').status_code in (
            status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

        assert new_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: {'foo': 'bar'}
        }).status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Test get 1 key
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(NODE_SELECTORS_JOBS, to_dict=True)

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_JOBS: {'foo': 'bar'}
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(NODE_SELECTORS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == {'foo': 'bar'}

        # Test get 2 key
        resp = self.auth_client.get(self.url + '?keys={}&keys={}'.format(
            node_selectors.NODE_SELECTORS_JOBS, node_selectors.NODE_SELECTORS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == [conf.get(NODE_SELECTORS_JOBS, to_dict=True),
                             conf.get(NODE_SELECTORS_BUILD_JOBS, to_dict=True)]
        # Test get wrong keys
        resp = self.auth_client.get(self.url + '?keys=secret1&keys=foo')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_update(self):
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) is None

        # Set new value
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: {'foo': 'bar'}
        })
        assert resp.status_code == status.HTTP_200_OK
        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) == {'foo': 'bar'}

        # Delete value
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: None
        })
        assert resp.status_code == status.HTTP_200_OK

        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) is None

        # Wrong key
        resp = self.auth_client.post(self.url, data={'foo': 'bar'})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.configs_mark
class TesOwnerConfigOptionsViewV1(BaseViewTest):
    serializer_class = ConfigOptionSerializer
    model_class = ConfigOption
    num_objects = 4
    HAS_AUTH = True
    ADMIN_USER = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.owner = self.get_owner()
        self.option_value1 = ConfigOption.objects.create(owner=self.owner,
                                                         key='value1',
                                                         value=2341)
        self.option_value2 = ConfigOption.objects.create(owner=self.owner,
                                                         key='value2',
                                                         value={'foo': 'bar'})
        self.option_secret1 = ConfigOption.objects.create(owner=self.owner,
                                                          key='secret1',
                                                          secret='secret1')
        self.option_secret2 = ConfigOption.objects.create(owner=self.owner,
                                                          key='secret2',
                                                          secret='secret2')
        self.url = self.get_url()
        self.queryset = self.model_class.objects.filter(owner=self.owner)

    def get_owner(self):
        return Owner.objects.get(name=Cluster.load().uuid)

    def get_url(self):
        return '/{}/{}/options/'.format(API_V1, self.owner.name)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Test get 1 key
        resp = self.auth_client.get(self.url + '?keys=value1')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == 1
        assert resp.data['next'] is None
        assert resp.data['results'][0] == ConfigOptionSerializer(self.option_value1).data

        # Test get 3 key
        resp = self.auth_client.get(self.url + '?keys=value1&keys=value2&keys=secret1')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == 3
        assert resp.data['next'] is None

        # Test get wrong keys
        resp = self.auth_client.get(self.url + '?keys=secret1&keys=foo')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == 1
        assert resp.data['next'] is None
        assert resp.data['results'][0] == ConfigOptionSerializer(self.option_secret1).data

    def test_create_update(self):
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) is None

        # Set new value
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: {'foo': 'bar'}
        })
        assert resp.status_code == status.HTTP_200_OK
        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) == {'foo': 'bar'}

        # Delete value
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: None
        })
        assert resp.status_code == status.HTTP_200_OK

        # Check value
        assert conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS) is None
