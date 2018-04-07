# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.initializations import ZerosInitializerConfig
from polyaxon_schemas.layers.advanced_activations import (
    ELUConfig,
    LeakyReLUConfig,
    PReLUConfig,
    ThresholdedReLUConfig
)


class TestAdvancedActivationConfigs(TestCase):
    def test_leaky_relu_config(self):
        config_dict = {
            'alpha': 0.3,
        }
        config = LeakyReLUConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_prelu_config(self):
        config_dict = {
            'alpha_initializer': ZerosInitializerConfig().to_schema(),
            'alpha_regularizer': None,
            'alpha_constraint': None,
            'shared_axes': None
        }
        config = PReLUConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_elu_config(self):
        config_dict = {
            'alpha': 0.1
        }
        config = ELUConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_thresholded_relu_config(self):
        config_dict = {
            'theta': 0.1
        }
        config = ThresholdedReLUConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
