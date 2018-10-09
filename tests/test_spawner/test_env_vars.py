from unittest import TestCase
from unittest.mock import MagicMock

import pytest

from kubernetes import client

from django.test import override_settings

from libs.api import API_HTTP_URL, API_WS_HOST
from scheduler.spawners.templates.env_vars import (
    EnvFromRefFoundError,
    get_env_from,
    get_env_var,
    get_from_secret,
    get_pod_env_from,
    get_resources_env_vars,
    get_service_env_vars,
    validate_configmap_refs,
    validate_secret_refs
)


@pytest.mark.spawner_mark
class TestEnvVars(TestCase):
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
        assert len(env_vars) == 9
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

    @override_settings(REFS_SECRETS=None)
    def test_validate_secret_refs_passes_if_not_specified(self):
        assert validate_secret_refs(secret_refs=[]) == []
        assert validate_secret_refs(secret_refs=None) == []

    @override_settings(REFS_SECRETS=None)
    def test_validate_secret_refs_raises_if_no_secret_refs_specified(self):
        with self.assertRaises(EnvFromRefFoundError):
            validate_secret_refs(secret_refs=['foo'])

        with self.assertRaises(EnvFromRefFoundError):
            validate_secret_refs(secret_refs=['foo', 'bar'])

    @override_settings(REFS_SECRETS=['foo', 'bar'])
    def test_validate_secret_refs_works_as_expected(self):
        assert validate_secret_refs(secret_refs=['foo']) == ['foo']
        assert validate_secret_refs(secret_refs=['foo', 'bar']) == ['foo', 'bar']

    @override_settings(REFS_CONFIG_MAPS=None)
    def test_validate_configmap_refs_passes_if_not_specified(self):
        assert validate_configmap_refs(configmap_refs=[]) == []
        assert validate_configmap_refs(configmap_refs=None) == []

    @override_settings(REFS_CONFIG_MAPS=None)
    def test_validate_configmap_refs_raises_if_no_secret_refs_specified(self):
        with self.assertRaises(EnvFromRefFoundError):
            validate_configmap_refs(configmap_refs=['foo'])

        with self.assertRaises(EnvFromRefFoundError):
            validate_configmap_refs(configmap_refs=['foo', 'bar'])

    @override_settings(REFS_CONFIG_MAPS=['foo', 'bar'])
    def test_validate_configmap_refs_works_as_expected(self):
        assert validate_configmap_refs(configmap_refs=['foo']) == ['foo']
        assert validate_configmap_refs(configmap_refs=['foo', 'bar']) == ['foo', 'bar']

    def test_get_env_from(self):
        with self.assertRaises(ValueError):
            get_env_from(secret_ref='foo', config_map_ref='bar')

        env_from_secret = get_env_from(secret_ref='foo')
        assert env_from_secret.secret_ref == 'foo'

        env_from_secret = get_env_from(config_map_ref='foo')
        assert env_from_secret.config_map_ref == 'foo'

    def test_get_pod_env_from(self):
        env_from = get_pod_env_from(secret_refs=['secret1', 'secret2'],
                                    configmap_refs=['config1', 'config2'])

        assert len(env_from) == 4
