# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.schemas.cli_configuration import CliConfigurationConfig


class TestCliConfigs(TestCase):
    def test_global_config(self):
        config_dict = {'check_count': 1}
        config = CliConfigurationConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
