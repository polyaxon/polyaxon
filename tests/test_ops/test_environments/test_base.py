# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.base import EnvironmentConfig
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
        config_dict['persistence'] = {
            'data': ['data1', 'data2'],
            'outputs': 'outputs1',
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add outputs
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

        # Add configmaps
        config_dict['configmap_refs'] = ['configmap1', 'configmap2']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
