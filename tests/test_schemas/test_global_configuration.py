# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.schemas.global_configuration import GlobalConfigurationConfig


class TestGlobalConfigs(TestCase):
    def test_global_config(self):
        config_dict = {'verbose': True,
                       'host': 'localhost',
                       'port': '80',
                       'verify_ssl': True,
                       'use_https': False}
        config = GlobalConfigurationConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
