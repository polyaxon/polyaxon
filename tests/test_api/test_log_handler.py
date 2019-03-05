# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.api.log_handler import LogHandlerConfig


class TestLogHandlerConfig(TestCase):
    def test_log_handler_config(self):
        config_dict = {'dsn': 'https//foo:bar',
                       'environment': 'staging',
                       'tags': {}}
        config = LogHandlerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
