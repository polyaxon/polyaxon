# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.layers.noise import (
    AlphaDropoutConfig,
    GaussianDropoutConfig,
    GaussianNoiseConfig
)


class TestNoiseConfigs(TestCase):
    def test_gaussian_noise_config(self):
        config_dict = {
            'stddev': 1.0
        }

        config = GaussianNoiseConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_gaussian_dropout_config(self):
        config_dict = {
            'rate': 0.8
        }

        config = GaussianDropoutConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_alpha_dropout_config(self):
        config_dict = {
            'rate': 0.8,
            'noise_shape': [1, 1],
            'seed': None
        }

        config = AlphaDropoutConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
