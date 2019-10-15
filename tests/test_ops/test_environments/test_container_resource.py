# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from tests.utils import assert_equal_dict

from schemas.ops.environments.container_resources import (
    ContainerResourcesConfig,
)


@pytest.mark.environment_mark
class TestContainerResourceConfigs(TestCase):
    def test_container_resource_config(self):
        config_dict = {"limits": {"cpu": 0.1}}
        config = ContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"requests": {"cpu": 0.1}}
        config = ContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {"requests": {"cpu": 0.1}, "limits": {"cpu": 0.1}}
        config = ContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "requests": {"cpu": 0.1, "memory": "10mi"},
            "limits": {"cpu": 0.1, "memory": 1024},
        }
        config = ContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "requests": {"cpu": 0.1, "memory": "10Mi", "amd.com/gpu": 2},
            "limits": {"cpu": 0.1, "memory": 1024, "amd.com/gpu": 2},
        }
        config = ContainerResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
