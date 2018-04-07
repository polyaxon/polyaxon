# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.logging import LoggingConfig


class TestLoggingConfigs(TestCase):
    def test_logging_config(self):
        config_dict = {
            'level': 'INFO',
            'formatter': None,
            'path': 'some/path/logging',
        }
        config = LoggingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
