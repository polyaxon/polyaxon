# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import MagicMock

from scheduler.spawners.templates.env_vars import get_resources_env_vars


class TestEnvVars(TestCase):
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
