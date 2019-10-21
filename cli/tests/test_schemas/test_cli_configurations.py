# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon.schemas.cli.cli_configuration import CliConfigurationConfig


class TestCliConfig(TestCase):
    def test_cli_config(self):
        config_dict = {
            "check_count": 1,
            "current_version": "0.0.1",
            "server_versions": {"cli": "0.0.1"},
            "log_handler": None,
        }
        config = CliConfigurationConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
