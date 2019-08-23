# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.pods import EnvironmentConfig


class TestEnvironmentsConfigs(TestCase):
    def test_environment_resources(self):
        config_dict = {
            'resources': {
                'requests': {'cpu': 0.5, 'memory': '256Mi', 'nvidia.com/gpu': 1, 'amd.com/gpu': 2},
                'limits': {'cpu': 1, 'memory': '400Mi', 'nvidia.com/gpu': 1, 'amd.com/gpu': 2},
            }
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_environment_config(self):
        config_dict = {
            'resources': {
                'requests': {'cpu': 0.5, 'memory': '256Mi'},
                'limits': {'cpu': 1, 'memory': '400Mi'},
            }
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add node selectors
        config_dict['node_selector'] = {
            'polyaxon.com': 'master',
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add labels
        config_dict['labels'] = {
            'foo': 'bar',
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add annotations
        config_dict['annotations'] = {
            'foo': 'bar',
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Outputs
        config_dict['outputs'] = {
            'jobs': ['data1.dfs', 34, 'data2'],
            'experiments': [1, 'outputs1', 2, 3],
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add secrets
        config_dict['secret_refs'] = ['secret1', 'secret2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add config_maps
        config_dict['config_map_refs'] = ['config_map1', 'config_map2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add service_account
        config_dict['service_account'] = 'service_account'
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add image_pull_secrets
        config_dict['image_pull_secrets'] = ['pull_secret1', 'pull_secret2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add env vars
        config_dict['env_vars'] = [['key', 'value']]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add security context per job
        config_dict['security_context'] = {'runAsUser': 1000, 'runAsGroup': 3000, 'fsGroup': 5000}
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add max_restarts
        config_dict['max_retries'] = 4
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add timeout
        config_dict['timeout'] = 4
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add restart_policy
        config_dict['restart_policy'] = 'never'
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add ttl
        config_dict['ttl'] = 40
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add data_refs
        config_dict['data_refs'] = [
            'data1',
            {'name': 'data2', 'mount': True},
            {'name': 'data3', 'paths': ['/subpath1', 'subpath2'], 'init': True}]
        config = EnvironmentConfig.from_dict(config_dict)
        # We remove this from the dict because the value is mutated every time it's parsed
        data_refs = config_dict.pop('data_refs')
        data_refs[0] = {'name': 'data1', 'init': True}
        assert data_refs == config.to_dict()['data_refs']

        # Add artifact_refs
        config_dict['artifact_refs'] = [
            'artifact1',
            {'name': 'artifact2', 'paths': ['/subpath1', 'subpath2'], 'init': True}
        ]
        config = EnvironmentConfig.from_dict(config_dict)
        # We remove this from the dict because the value is mutated every time it's parsed
        artifact_refs = config_dict.pop('artifact_refs')
        artifact_refs[0] = {'name': 'artifact1', 'init': True}
        assert artifact_refs == config.to_dict()['artifact_refs']
