# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ml.rl.environments import GymEnvironmentConfig
from polyaxon_schemas.ml.rl.explorations import (
    ConstantExplorationConfig,
    DecayExplorationConfig,
    GreedyExplorationConfig,
    OrnsteinUhlenbeckExplorationConfig,
    RandomDecayExplorationConfig,
    RandomExplorationConfig
)
from polyaxon_schemas.ml.rl.memories import BatchMemoryConfig


class TestMemoryConfigs(TestCase):
    def test_latent_bridge_config(self):
        config_dict = {
            'env_id': 'CartPole-v0',
        }
        config = GymEnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)


class TestEnvironmentConfigs(TestCase):
    def test_latent_bridge_config(self):
        config_dict = {
            'size': 500,
            'batch_size': 500,
        }
        config = BatchMemoryConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)


class TestExplorationConfigs(TestCase):
    def test_constant_exploration_config(self):
        config_dict = {
            'value': 0.8,
            'is_continuous': False
        }
        config = ConstantExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_greedy_exploration_config(self):
        config_dict = {
            'is_continuous': False
        }
        config = GreedyExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_random_exploration_config(self):
        config_dict = {
            'is_continuous': False
        }
        config = RandomExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_decay_exploration_config(self):
        config_dict = {
            'is_continuous': False,
            'exploration_rate': 0.15,
            'decay_type': 'polynomial_decay',
            'start_decay_at': 0,
            'stop_decay_at': 1e9,
            'decay_rate': 0.,
            'staircase': False,
            'decay_steps': 100000,
            'min_exploration_rate': 0
        }
        config = DecayExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_random_decay_exploration_config(self):
        config_dict = {
            'is_continuous': False,
            'num_actions': None,
            'decay_type': 'polynomial_decay',
            'start_decay_at': 0,
            'stop_decay_at': 1e9,
            'decay_rate': 0.,
            'staircase': False,
            'decay_steps': 10000,
            'min_exploration_rate': 0
        }
        config = RandomDecayExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_orsteinuhlenbeck_exploration_config(self):
        config_dict = {
            'is_continuous': True,
            'num_actions': 4,
            'sigma': 0.3,
            'mu': 0,
            'theta': 0.15
        }
        config = OrnsteinUhlenbeckExplorationConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
