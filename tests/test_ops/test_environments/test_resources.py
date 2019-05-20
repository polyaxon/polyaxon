# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.resources import (
    K8SContainerResourcesConfig,
    K8SResourcesConfig,
    PodResourcesConfig
)


class TestResourcesConfigs(TestCase):
    def test_k8s_resources_config(self):
        config_dict = {
            'requests': 0.8,
            'limits': 1,
        }
        config = K8SResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_container_resources_config(self):
        config_dict = {
            'requests': {
                'cpu': 0.8,
                'gpu': 2,
                'tpu': 2,
                'memory': 265
            },
            'limits': {
                'cpu': 1,
                'gpu': 4,
                'tpu': 4,
                'memory': 512
            }
        }
        config = K8SContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict = {
            'requests': {
                'cpu': '800m',
                'gpu': 2,
                'tpu': 2,
                'memory': '100Ki'
            },
            'limits': {
                'cpu': 1,
                'tpu': 4,
                'memory': '100Mi'
            }
        }
        config = K8SContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict = {
            'requests': {
                'cpu': '800m',
                'tpu': 2,
                'memory': '100Ki'
            },
            'limits': {
                'cpu': 1,
            }
        }
        config = K8SContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict = {'limits': {'cpu': 0.1}}
        config = K8SContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_pod_resources_config(self):
        config_dict = {
            'cpu': {
                'requests': 0.8,
                'limits': 1
            },
            'gpu': {
                'requests': 2,
                'limits': 4
            },
            'tpu': {
                'requests': 2,
                'limits': 4
            },
            'memory': {
                'requests': 265,
                'limits': 512
            },
        }
        config = PodResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_pod_resources_add(self):
        config_dict1 = {
            'cpu': {
                'requests': 0.8,
            },
            'gpu': {
                'requests': 2,
            },
            'tpu': {
                'requests': 2,
                'limits': 4
            },
            'memory': {
                'requests': 200,
                'limits': 300
            },
        }

        config_dict2 = {
            'gpu': {
                'limits': 4
            },
            'tpu': {
                'requests': 2,
            },
            'memory': {
                'requests': 300,
                'limits': 200
            },
        }
        config1 = PodResourcesConfig.from_dict(config_dict1)
        config2 = PodResourcesConfig.from_dict(config_dict2)

        config = config1 + config2
        assert config.cpu.to_dict() == {'requests': 0.8}
        assert config.memory.to_dict() == {'requests': 500, 'limits': 500}
        assert config.gpu.to_dict() == {'requests': 2, 'limits': 4}
        assert config.tpu.to_dict() == {'requests': 4, 'limits': 4}
