# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.group.early_stopping_policies import EarlyStoppingConfig
from polyaxon_schemas.ops.group.metrics import Optimization


class TestEarlyStoppingConfigs(TestCase):

    def test_early_stopping(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
        }
        config = EarlyStoppingConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict.pop('optimization') == Optimization.MAXIMIZE
        assert_equal_dict(config_to_dict, config_dict)

    def test_early_stopping_with_median_policy(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
            'optimization': Optimization.MINIMIZE,
            'policy': {'kind': 'median', 'evaluation_interval': 1}
        }
        config = EarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_early_stopping_with_average_policy(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
            'optimization': Optimization.MINIMIZE,
            'policy': {'kind': 'average', 'evaluation_interval': 1}
        }
        config = EarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_early_stopping_with_truncation_policy(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
            'optimization': Optimization.MAXIMIZE,
            'policy': {'kind': 'truncation', 'percent': 50, 'evaluation_interval': 1}
        }
        config = EarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
