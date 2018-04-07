# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow.exceptions import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.settings import EarlyStoppingMetricConfig, SettingsConfig
from polyaxon_schemas.utils import EarlyStoppingPolicy, Optimization


class TestSettingConfigs(TestCase):

    def test_early_stopping(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
            'optimization': Optimization.MINIMIZE,
            'policy': EarlyStoppingPolicy.ALL
        }
        config = EarlyStoppingMetricConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_settings_config(self):
        config_dict = {
            'logging': LoggingConfig().to_dict(),
            'concurrent_experiments': 2,
        }
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add n_experiments
        config_dict['random_search'] = {'n_experiments': 10}
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict['random_search']['n_experiments'] = -5
        with self.assertRaises(ValidationError):
            SettingsConfig.from_dict(config_dict)

        config_dict['random_search']['n_experiments'] = -0.5
        with self.assertRaises(ValidationError):
            SettingsConfig.from_dict(config_dict)

        # Add n_experiments percent
        config_dict['random_search']['n_experiments'] = 0.5
        with self.assertRaises(ValidationError):
            SettingsConfig.from_dict(config_dict)

        config_dict['random_search']['n_experiments'] = 5
        # Add early stopping
        config_dict['early_stopping'] = [
            {
                'metric': 'loss',
                'value': 0.1,
                'optimization': Optimization.MINIMIZE,
                'policy': EarlyStoppingPolicy.ALL
            },
            {
                'metric': 'accuracy',
                'value': 0.9,
                'optimization': Optimization.MAXIMIZE,
                'policy': EarlyStoppingPolicy.EXPERIMENT
            }
        ]
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
