from unittest import TestCase
from unittest.mock import MagicMock

from kubernetes import client

from libs.api import API_KEY_NAME
from scheduler.spawners.templates.env_vars import (
    get_env_var,
    get_from_app_secret,
    get_resources_env_vars,
    get_service_env_vars
)


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

    def test_get_from_app_secret(self):
        env_var = get_from_app_secret(key_name='foo',
                                      secret_key_name='secret_key',
                                      secret_ref_name='secret_ref')
        assert env_var.name == 'foo'
        assert isinstance(env_var.value_from, client.V1EnvVarSource)
        assert env_var.value_from.secret_key_ref.name == 'secret_ref'
        assert env_var.value_from.secret_key_ref.key == 'secret_key'

    def test_get_service_env_vars(self):
        env_vars = get_service_env_vars()
        assert len(env_vars) == 6
        env_var_names = [env_var.name for env_var in env_vars]
        assert 'POLYAXON_K8S_NAMESPACE' in env_var_names
        assert 'POLYAXON_SECRET_KEY' in env_var_names
        assert 'POLYAXON_INTERNAL_SECRET_TOKEN' in env_var_names
        assert 'POLYAXON_RABBITMQ_PASSWORD' in env_var_names
        assert 'POLYAXON_DB_PASSWORD' in env_var_names
        assert API_KEY_NAME in env_var_names

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
