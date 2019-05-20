# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.pods import EnvironmentConfig
from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig


class TestEnvironmentsConfigs(TestCase):

    def test_environment_config(self):
        config_dict = {
            'resources': PodResourcesConfig(cpu=K8SResourcesConfig(0.5, 1)).to_dict()
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add node selectors
        config_dict['node_selector'] = {
            'polyaxon.com': 'master',
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add persistence
        config_dict['data_refs'] = ['data1', 'data2']
        config_dict['artifact_refs'] = ['outputs1']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # TODO: Add outputs
        # config_dict['outputs'] = {
        #     'jobs': ['data1.dfs', 34, 'data2'],
        #     'experiments': [1, 'outputs1', 2, 3],
        # }
        # config = EnvironmentConfig.from_dict(config_dict)
        # assert_equal_dict(config_dict, config.to_dict())

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

        # Add max_restarts
        config_dict['max_restarts'] = 4
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add data_refs
        config_dict['data_refs'] = ['data1', 'data2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add artifact_refs
        config_dict['artifact_refs'] = ['artifact1', 'artifact2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
