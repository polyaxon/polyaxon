# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ml.optimizers import (
    AdadeltaConfig,
    AdagradConfig,
    AdamConfig,
    FtrlConfig,
    MomentumConfig,
    NestrovConfig,
    RMSPropConfig,
    SGDConfig
)


class TestOptimizerConfigs(TestCase):
    def test_sgd_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = SGDConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_momentum_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'momentum': 0.8,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = MomentumConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_nestrov_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'momentum': 0.8,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = NestrovConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_rmsprop_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'momentum': 0.,
            'decay': 0.9,
            'epsilon': 1e-10,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = RMSPropConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_adam_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'beta1': 0.9,
            'beta2': 0.999,
            'epsilon': 1e-10,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = AdamConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_adagrad_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'initial_accumulator_value': 0.1,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = AdagradConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_adadelta_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'epsilon': 1e-08,
            'rho': 0.95,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = AdadeltaConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_ftrl_config(self):
        config_dict = {
            'learning_rate': 0.001,
            'initial_accumulator_value': 0.1,
            'l1_regularization_strength': 0.0,
            'l2_regularization_strength': 0.0,
            'learning_rate_power': -0.5,
            'decay_type': "",
            'decay_rate': 0.,
            'decay_steps': 100,
            'start_decay_at': 0,
            'stop_decay_at': 1e10,
            'min_learning_rate': 1e-12,
            'staircase': False,
            'global_step': None,
            'use_locking': False,
            'name': 'optimizer'
        }
        config = FtrlConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
