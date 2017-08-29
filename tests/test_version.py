# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.version import CliVersionConfig


class TestProjectConfigs(TestCase):
    def test_project_config(self):
        config_dict = {'latest_version': '2.2.2', 'min_version': '1.1.0'}
        config = CliVersionConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
