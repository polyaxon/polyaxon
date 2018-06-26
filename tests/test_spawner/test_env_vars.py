# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import MagicMock

from scheduler.spawners.templates.env_vars import get_resources_env_vars


class TestEnvVars(TestCase):
    def test_get_resources_env_vars(self):
        vars = get_resources_env_vars(None)
        assert len(vars)
        assert vars[0].name == 'NVIDIA_VISIBLE_DEVICES'
        assert vars[0].value == 'none'

        resources = MagicMock()
        resources.gpu = None
        vars = get_resources_env_vars(resources)
        assert len(vars)
        assert vars[0].name == 'NVIDIA_VISIBLE_DEVICES'
        assert vars[0].value == 'none'

        resources = MagicMock()
        resources.gpu.limits = '0'
        vars = get_resources_env_vars(resources)
        assert len(vars)
        assert vars[0].name == 'NVIDIA_VISIBLE_DEVICES'
        assert vars[0].value == 'none'
