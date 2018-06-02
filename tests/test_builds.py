# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.builds import BuildJobConfig


class TestBuildConfigs(TestCase):
    def test_build_config(self):
        config_dict = {
            'config': {'k': 'v'},
        }
        config = BuildJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict
