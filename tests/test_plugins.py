# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.plugins import PluginJobConfig


class TestPluginConfigs(TestCase):
    def test_plugin_config(self):
        config_dict = {
            'config': {'k': 'v'},
        }
        config = PluginJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict
