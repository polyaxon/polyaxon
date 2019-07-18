from unittest.mock import MagicMock

import pytest

from kubernetes import client

from factories.factory_k8s_config_maps import K8SConfigMapFactory
from factories.factory_k8s_secrets import K8SSecretFactory
from libs.api import API_HTTP_URL, API_WS_HOST
from polypod.templates.env_vars import (
    EnvFromRefFoundError,
    get_env_from,
    get_env_var,
    get_from_secret,
    get_pod_env_from,
    get_pod_env_from_config_maps,
    get_pod_env_from_secrets,
    get_resources_env_vars,
    get_service_env_vars,
    get_str_var
)
from tests.base.case import BaseTest


@pytest.mark.spawner_mark
class TestEnvVars(BaseTest):
    def test_env_vars(self):
        # String value
        env_var = get_env_var(name='foo', value='bar')
        assert env_var.name == 'foo'
        assert env_var.value == 'bar'
        # Int value
        env_var = get_env_var(name='foo', value=1)
        assert env_var.name == 'foo'
        assert env_var.value == '1'
        # Dict value
        env_var = get_env_var(name='foo', value={'moo': 'bar'})
        assert env_var.name == 'foo'
        assert env_var.value == '{"moo": "bar"}'

    def test_str_var(self):
        # String value
        var = get_str_var(value='bar')
        assert var == 'bar'
        # Int value
        var = get_str_var(value=1)
        assert var == '1'
        # Dict value
        var = get_str_var(value={'moo': 'bar'})
        assert var == '{"moo": "bar"}'
        # Empty value
        var = get_str_var(value=None)
        assert var == ''
        # 0 value
        var = get_str_var(value=0)
        assert var == '0'

    def test_get_from_secret(self):
        env_var = get_from_secret(key_name='foo',
                                  secret_key_name='secret_key',
                                  secret_ref_name='secret_ref')
        assert env_var.name == 'foo'
        assert isinstance(env_var.value_from, client.V1EnvVarSource)
        assert env_var.value_from.secret_key_ref.name == 'secret_ref'
        assert env_var.value_from.secret_key_ref.key == 'secret_key'

    def test_get_service_env_vars(self):
        env_vars = get_service_env_vars()
        assert len(env_vars) == 10
        env_var_names = [env_var.name for env_var in env_vars]
        assert 'POLYAXON_K8S_NAMESPACE' in env_var_names
        assert 'POLYAXON_SECRET_KEY' in env_var_names
        assert 'POLYAXON_SECRET_INTERNAL_TOKEN' in env_var_names
        assert 'POLYAXON_RABBITMQ_PASSWORD' in env_var_names
        assert 'POLYAXON_DB_PASSWORD' in env_var_names
        assert API_HTTP_URL in env_var_names
        assert API_WS_HOST in env_var_names

    def test_get_resources_env_vars(self):
        env_vars = get_resources_env_vars(None)
        assert any(item.name == 'NVIDIA_VISIBLE_DEVICES' and item.value == 'none'
                   for item in env_vars)

        resources = MagicMock()
        resources.gpu = None
        env_vars = get_resources_env_vars(resources)
        assert any(item.name == 'NVIDIA_VISIBLE_DEVICES' and item.value == 'none'
                   for item in env_vars)

        resources = MagicMock()
        resources.gpu.limits = '0'
        env_vars = get_resources_env_vars(resources)
        assert any(item.name == 'NVIDIA_VISIBLE_DEVICES' and item.value == 'none'
                   for item in env_vars)

    def test_validate_secret_refs_passes_if_not_specified(self):
        assert get_pod_env_from_secrets(secret_refs=[]) == []
        assert get_pod_env_from_secrets(secret_refs=None) == []

    def test_validate_secret_refs_raises_if_no_secret_refs_specified(self):
        with self.assertRaises(EnvFromRefFoundError):
            get_pod_env_from_secrets(secret_refs=['foo'])

        with self.assertRaises(EnvFromRefFoundError):
            get_pod_env_from_secrets(secret_refs=['foo', 'bar'])

    def test_validate_secret_refs_works_as_expected(self):
        K8SSecretFactory(name='foo', k8s_ref='foo')
        K8SSecretFactory(name='bar', k8s_ref='bar')
        results = get_pod_env_from_secrets(secret_refs=['foo'])
        assert len(results) == 1
        assert results[0].secret_ref == {'name': 'foo'}
        results = get_pod_env_from_secrets(secret_refs=['foo', 'bar'])
        assert len(results) == 2
        assert results[0].secret_ref == {'name': 'foo'}
        assert results[1].secret_ref == {'name': 'bar'}

    def test_validate_config_map_refs_passes_if_not_specified(self):
        assert get_pod_env_from_config_maps(config_map_refs=[]) == []
        assert get_pod_env_from_config_maps(config_map_refs=None) == []

    def test_validate_config_map_refs_raises_if_no_secret_refs_specified(self):
        with self.assertRaises(EnvFromRefFoundError):
            get_pod_env_from_config_maps(config_map_refs=['foo'])

        with self.assertRaises(EnvFromRefFoundError):
            get_pod_env_from_config_maps(config_map_refs=['foo', 'bar'])

    def test_validate_config_map_refs_works_as_expected(self):
        K8SConfigMapFactory(name='foo', k8s_ref='foo')
        K8SConfigMapFactory(name='bar', k8s_ref='bar')
        results = get_pod_env_from_config_maps(config_map_refs=['foo'])
        assert len(results) == 1
        assert results[0].config_map_ref == {'name': 'foo'}
        results = get_pod_env_from_config_maps(config_map_refs=['foo', 'bar'])
        assert len(results) == 2
        assert results[0].config_map_ref == {'name': 'foo'}
        assert results[1].config_map_ref == {'name': 'bar'}

    def test_get_env_from(self):
        with self.assertRaises(ValueError):
            get_env_from(secret_ref='foo', config_map_ref='bar')

        with self.assertRaises(ValueError):
            get_env_from(secret_ref=None)

        with self.assertRaises(ValueError):
            get_env_from(config_map_ref=None)

        env_from_secret = get_env_from(secret_ref='foo')
        assert env_from_secret.secret_ref == {'name': 'foo'}

        env_from_secret = get_env_from(config_map_ref='foo')
        assert env_from_secret.config_map_ref == {'name': 'foo'}

    def test_get_pod_env_from(self):
        K8SSecretFactory(name='secret1', k8s_ref='secret1')
        K8SSecretFactory(name='secret2', k8s_ref='secret2', items=['key1', 'key2'])
        K8SConfigMapFactory(name='config1', k8s_ref='config1')
        K8SConfigMapFactory(name='config2', k8s_ref='config2', items=['key1', 'key2'])
        env_from = get_pod_env_from(secret_refs=['secret1', 'secret2'],
                                    config_map_refs=['config1', 'config2'])

        assert len(env_from) == 4
