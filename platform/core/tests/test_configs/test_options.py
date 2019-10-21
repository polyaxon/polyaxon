# pylint:disable=too-many-lines
# pylint:disable=too-many-statements
import pytest

from rest_framework import status

import conf

from constants.urls import API_V1
from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from options.registry import (
    affinities,
    auth_azure,
    auth_bitbucket,
    auth_github,
    auth_gitlab,
    env_vars,
    integrations,
    k8s,
    k8s_config_maps,
    k8s_secrets,
    node_selectors,
    notebooks,
    service_accounts,
    tensorboards,
    tolerations
)
from tests.base.views import BaseViewTest


@pytest.mark.configs_mark
class TestOptionsSaveLoad(BaseViewTest):
    model_class = ConfigOption
    HAS_AUTH = True
    ADMIN_USER = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.owner = self.get_owner()
        self.url = self.get_url()
        self.queryset = self.model_class.objects.filter(owner=self.owner)

    def get_owner(self):
        return Cluster.get_or_create_owner(Cluster.load())

    def get_url(self):
        return '/{}/options/'.format(API_V1)

    def test_node_selectors(self):
        data = {'foo': 'bar'}

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            node_selectors.NODE_SELECTORS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            node_selectors.NODE_SELECTORS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(node_selectors.NODE_SELECTORS_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_affinities(self):
        data = {'podAffinity': {'preferredDuringSchedulingIgnoredDuringExecution:': []}}

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            affinities.AFFINITIES_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            affinities.AFFINITIES_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            affinities.AFFINITIES_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            affinities.AFFINITIES_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            affinities.AFFINITIES_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            affinities.AFFINITIES_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(affinities.AFFINITIES_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_tolerations(self):
        data = [{'key': "key", 'operator': "Equal", 'value': "value", 'effect': "NoSchedule"}]

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            tolerations.TOLERATIONS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            tolerations.TOLERATIONS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            tolerations.TOLERATIONS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            tolerations.TOLERATIONS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            tolerations.TOLERATIONS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tolerations.TOLERATIONS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tolerations.TOLERATIONS_TENSORBOARDS, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_service_accounts(self):
        data = 'service-foo'

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            service_accounts.SERVICE_ACCOUNTS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            service_accounts.SERVICE_ACCOUNTS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            service_accounts.SERVICE_ACCOUNTS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            service_accounts.SERVICE_ACCOUNTS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            service_accounts.SERVICE_ACCOUNTS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            service_accounts.SERVICE_ACCOUNTS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(service_accounts.SERVICE_ACCOUNTS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] == data

    def test_config_maps(self):
        data = ['config1', 'config2']

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            k8s_config_maps.K8S_CONFIG_MAPS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_config_maps.K8S_CONFIG_MAPS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_config_maps.K8S_CONFIG_MAPS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_config_maps.K8S_CONFIG_MAPS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_config_maps.K8S_CONFIG_MAPS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_config_maps.K8S_CONFIG_MAPS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_config_maps.K8S_CONFIG_MAPS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] == data

    def test_secrets(self):
        data = ['secret1', 'secret2']

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            k8s_secrets.K8S_SECRETS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_secrets.K8S_SECRETS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_secrets.K8S_SECRETS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_secrets.K8S_SECRETS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            k8s_secrets.K8S_SECRETS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s_secrets.K8S_SECRETS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s_secrets.K8S_SECRETS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] == data

    def test_env_vars(self):
        data = [['key1', 'value1'], ['key2', 'value2']]

        # Build
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            env_vars.ENV_VARS_BUILD_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_BUILD_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_BUILD_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Job
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_JOBS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            env_vars.ENV_VARS_JOBS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_JOBS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_JOBS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Experiment
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            env_vars.ENV_VARS_EXPERIMENTS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_EXPERIMENTS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_EXPERIMENTS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Notebook
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            env_vars.ENV_VARS_NOTEBOOKS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_NOTEBOOKS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_NOTEBOOKS, to_dict=True)
        assert resp.data[0]['value'] == data

        # Tensorboard
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] is None

        # Update node selectors
        resp = self.auth_client.post(self.url, data={
            env_vars.ENV_VARS_TENSORBOARDS: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            env_vars.ENV_VARS_TENSORBOARDS))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(env_vars.ENV_VARS_TENSORBOARDS,
                                        to_dict=True)
        assert resp.data[0]['value'] == data

    def test_auth_github(self):
        # enabled
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is False

        resp = self.auth_client.post(self.url, data={
            auth_github.AUTH_GITHUB_ENABLED: True
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is True

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 0

        resp = self.auth_client.post(self.url, data={
            auth_github.AUTH_GITHUB_VERIFICATION_SCHEDULE: 2
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 2

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_github.AUTH_GITHUB_CLIENT_ID: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client secret
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_github.AUTH_GITHUB_CLIENT_SECRET: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_github.AUTH_GITHUB_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_github.AUTH_GITHUB_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

    def test_auth_bitbucket(self):
        # enabled
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is False

        resp = self.auth_client.post(self.url, data={
            auth_bitbucket.AUTH_BITBUCKET_ENABLED: True
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is True

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_VERIFICATION_SCHEDULE,
                                        to_dict=True)
        assert resp.data[0]['value'] == 0

        resp = self.auth_client.post(self.url, data={
            auth_bitbucket.AUTH_BITBUCKET_VERIFICATION_SCHEDULE: 2
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_VERIFICATION_SCHEDULE,
                                        to_dict=True)
        assert resp.data[0]['value'] == 2

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_ID: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client secret
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_SECRET: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_bitbucket.AUTH_BITBUCKET_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_bitbucket.AUTH_BITBUCKET_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

    def test_auth_gitlab(self):
        # enabled
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is False

        resp = self.auth_client.post(self.url, data={
            auth_gitlab.AUTH_GITLAB_ENABLED: True
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is True

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 0

        resp = self.auth_client.post(self.url, data={
            auth_gitlab.AUTH_GITLAB_VERIFICATION_SCHEDULE: 2
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 2

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_gitlab.AUTH_GITLAB_CLIENT_ID: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client secret
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_gitlab.AUTH_GITLAB_CLIENT_SECRET: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client url
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_URL))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_URL, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_gitlab.AUTH_GITLAB_URL: 'https://gitlab.com'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_gitlab.AUTH_GITLAB_URL))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_gitlab.AUTH_GITLAB_URL, to_dict=True)
        assert resp.data[0]['value'] == 'https://gitlab.com'

    def test_auth_azure(self):
        # enabled
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is False

        resp = self.auth_client.post(self.url, data={
            auth_azure.AUTH_AZURE_ENABLED: True
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_ENABLED))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_ENABLED, to_dict=True)
        assert resp.data[0]['value'] is True

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 0

        resp = self.auth_client.post(self.url, data={
            auth_azure.AUTH_AZURE_VERIFICATION_SCHEDULE: 2
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_VERIFICATION_SCHEDULE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_VERIFICATION_SCHEDULE, to_dict=True)
        assert resp.data[0]['value'] == 2

        # client id
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_azure.AUTH_AZURE_CLIENT_ID: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_CLIENT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_CLIENT_ID, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client secret
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_azure.AUTH_AZURE_CLIENT_SECRET: 'foobar'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_CLIENT_SECRET))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_CLIENT_SECRET, to_dict=True)
        assert resp.data[0]['value'] == 'foobar'

        # client url
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_TENANT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_TENANT_ID, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            auth_azure.AUTH_AZURE_TENANT_ID: 'some_value'
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            auth_azure.AUTH_AZURE_TENANT_ID))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(auth_azure.AUTH_AZURE_TENANT_ID, to_dict=True)
        assert resp.data[0]['value'] == 'some_value'

    def test_integrations(self):
        data = [
            {'url': 'https://hooks.com/services/sdfdfdsfsdf/sdflsdklfj'},
            {'url': ' https://hooks.com/services/sdlkfjsdlk/lkjsdlkfjdklsjf2'}
        ]

        # Discord
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_DISCORD))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_DISCORD, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_DISCORD: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_DISCORD))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_DISCORD, to_dict=True)
        assert resp.data[0]['value'] == data

        # Hipchat
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_HIPCHAT))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_HIPCHAT, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_HIPCHAT: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_HIPCHAT))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_HIPCHAT, to_dict=True)
        assert resp.data[0]['value'] == data

        # Mattermost
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_MATTERMOST))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_MATTERMOST, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_MATTERMOST: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_MATTERMOST))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_MATTERMOST, to_dict=True)
        assert resp.data[0]['value'] == data

        # Pagerduty
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_PAGER_DUTY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_PAGER_DUTY, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_PAGER_DUTY: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_PAGER_DUTY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_PAGER_DUTY, to_dict=True)
        assert resp.data[0]['value'] == data

        # Slack
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_SLACK))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_SLACK, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_SLACK: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_SLACK))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_SLACK, to_dict=True)
        assert resp.data[0]['value'] == data

        # Generic
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_GENERIC))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_GENERIC, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            integrations.INTEGRATIONS_WEBHOOKS_GENERIC: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            integrations.INTEGRATIONS_WEBHOOKS_GENERIC))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(integrations.INTEGRATIONS_WEBHOOKS_GENERIC, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_k8s(self):
        # GPU
        data = 'something.com/gpu'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_GPU_RESOURCE_KEY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_GPU_RESOURCE_KEY, to_dict=True)
        assert resp.data[0]['value'] == 'nvidia.com/gpu'

        resp = self.auth_client.post(self.url, data={
            k8s.K8S_GPU_RESOURCE_KEY: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_GPU_RESOURCE_KEY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_GPU_RESOURCE_KEY, to_dict=True)
        assert resp.data[0]['value'] == data

        # TPU tf version
        data = '1.14'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_TPU_TF_VERSION))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_TPU_TF_VERSION, to_dict=True)
        assert resp.data[0]['value'] == '1.12'

        resp = self.auth_client.post(self.url, data={
            k8s.K8S_TPU_TF_VERSION: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_TPU_TF_VERSION))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_TPU_TF_VERSION, to_dict=True)
        assert resp.data[0]['value'] == data

        # TPU tf version
        data = 'cloud-tpus.google.com/preemptible-v2'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_TPU_RESOURCE_KEY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_TPU_RESOURCE_KEY, to_dict=True)
        assert resp.data[0]['value'] == 'cloud-tpus.google.com/v2'

        resp = self.auth_client.post(self.url, data={
            k8s.K8S_TPU_RESOURCE_KEY: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            k8s.K8S_TPU_RESOURCE_KEY))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(k8s.K8S_TPU_RESOURCE_KEY, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_notebooks(self):
        # Backend
        data = 'lab'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            notebooks.NOTEBOOKS_BACKEND))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(notebooks.NOTEBOOKS_BACKEND, to_dict=True)
        assert resp.data[0]['value'] == 'notebook'

        resp = self.auth_client.post(self.url, data={
            notebooks.NOTEBOOKS_BACKEND: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            notebooks.NOTEBOOKS_BACKEND))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(notebooks.NOTEBOOKS_BACKEND, to_dict=True)
        assert resp.data[0]['value'] == data

        # Docker image
        data = 'someimage:tag-12'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            notebooks.NOTEBOOKS_DOCKER_IMAGE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(notebooks.NOTEBOOKS_DOCKER_IMAGE, to_dict=True)
        assert resp.data[0]['value'] is None

        resp = self.auth_client.post(self.url, data={
            notebooks.NOTEBOOKS_DOCKER_IMAGE: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            notebooks.NOTEBOOKS_DOCKER_IMAGE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(notebooks.NOTEBOOKS_DOCKER_IMAGE, to_dict=True)
        assert resp.data[0]['value'] == data

    def test_tensorboards(self):
        # Docker image
        data = 'someimage:tag-12'
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tensorboards.TENSORBOARDS_DOCKER_IMAGE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tensorboards.TENSORBOARDS_DOCKER_IMAGE, to_dict=True)
        assert resp.data[0]['value'] == 'tensorflow/tensorflow:1.11.0-py3'

        resp = self.auth_client.post(self.url, data={
            tensorboards.TENSORBOARDS_DOCKER_IMAGE: data
        })
        assert resp.status_code == status.HTTP_200_OK
        resp = self.auth_client.get(self.url + '?keys={}'.format(
            tensorboards.TENSORBOARDS_DOCKER_IMAGE))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data[0] == conf.get(tensorboards.TENSORBOARDS_DOCKER_IMAGE, to_dict=True)
        assert resp.data[0]['value'] == data
