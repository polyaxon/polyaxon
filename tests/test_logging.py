# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.logging import LoggingConfig
from tests.utils import assert_equal_dict


class TestLoggingConfigs(TestCase):
    def test_logging_config(self):
        config_dict = {
            'level': 'INFO',
            'formatter': None,
            'path': 'some/path/logging',
            'save_summary_steps': 10,
            'save_checkpoints_secs': None,
            'save_checkpoints_steps': None,
            'keep_checkpoint_max': 5,
            'keep_checkpoint_every_n_hours': 10000
        }
        config = LoggingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
