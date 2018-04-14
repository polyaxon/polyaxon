# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow.exceptions import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.settings import (
    EarlyStoppingMetricConfig,
    GridSearchConfig,
    HyperbandConfig,
    RandomSearchConfig,
    SearchMetricConfig,
    SettingsConfig
)
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

    def test_grid_search_config(self):
        config_dict = {'n_experiments': 10}
        config = GridSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict['n_experiments'] = -5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        config_dict['n_experiments'] = -0.5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        # Add n_experiments percent
        config_dict['n_experiments'] = 0.5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        config_dict['n_experiments'] = 5
        config = GridSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_random_search_config(self):
        config_dict = {'n_experiments': 10}
        config = RandomSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict['n_experiments'] = -5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        config_dict['n_experiments'] = -0.5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        # Add n_experiments percent
        config_dict['n_experiments'] = 0.5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        config_dict['n_experiments'] = 5
        config = RandomSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_hyperband_config(self):
        config_dict = {
            'max_iter': 10,
            'eta': 3,
            'resource': 'steps',
            'metric': SearchMetricConfig(name='loss', optimization=Optimization.MINIMIZE).to_dict()
        }
        config = HyperbandConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict['max_iter'] = 0
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict['max_iter'] = -0.5
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict['max_iter'] = 3
        # Add n_experiments percent
        config_dict['eta'] = -0.5
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict['eta'] = 2.9
        config = HyperbandConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_settings_random_search_config(self):
        config_dict = {
            'logging': LoggingConfig().to_dict(),
            'concurrent_experiments': 2,
        }
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add random_search
        config_dict['random_search'] = {'n_experiments': 10}
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add grid_search should raise
        config_dict['grid_search'] = {'n_experiments': 10}
        with self.assertRaises(ValidationError):
            SettingsConfig.from_dict(config_dict)

        # Remove random_search should pass
        del config_dict['random_search']
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add hyperband should raise
        config_dict['hyperband'] = {
            'max_iter': 10,
            'eta': 3,
            'resource': 'steps',
            'metric': SearchMetricConfig(name='loss', optimization=Optimization.MINIMIZE).to_dict()
        }
        with self.assertRaises(ValidationError):
            SettingsConfig.from_dict(config_dict)

        # Remove random_search should pass
        del config_dict['grid_search']
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

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
