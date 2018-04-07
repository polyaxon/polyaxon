# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.bridges import LatentBridgeConfig, NoOpBridgeConfig


class TestConstraintConfigs(TestCase):
    def test_latent_bridge_config(self):
        config_dict = {
            'state_size': [2, 2],
            'latent_dim': 1,
            'mean': 1.,
            'stddev': 0.,
            'name': 'latent',
        }
        config = LatentBridgeConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_noop_bridge_config(self):
        config_dict = {
            'state_size': [2, 2],
            'name': 'noop',
        }
        config = NoOpBridgeConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
