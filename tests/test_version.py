# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.version import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    PlatformVersionConfig
)


class TestVersionConfigs(TestCase):
    def test_cli_version_config(self):
        config_dict = {'latest_version': '2.2.2', 'min_version': '1.1.0'}
        config = CliVersionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_platform_version_config(self):
        config_dict = {'latest_version': '2.2.2', 'min_version': '1.1.0'}
        config = PlatformVersionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_lib_version_config(self):
        config_dict = {'latest_version': '2.2.2', 'min_version': '1.1.0'}
        config = LibVersionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_chart_version_config(self):
        config_dict = {'version': '2.2.2'}
        config = ChartVersionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
