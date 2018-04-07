# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.initializations import GlorotNormalInitializerConfig, ZerosInitializerConfig
from polyaxon_schemas.layers.core import (
    ActivationConfig,
    ActivityRegularizationConfig,
    CastConfig,
    DenseConfig,
    DropoutConfig,
    FlattenConfig,
    MaskingConfig,
    PermuteConfig,
    RepeatVectorConfig,
    ReshapeConfig,
    SpatialDropout1DConfig,
    SpatialDropout2DConfig,
    SpatialDropout3DConfig
)


class TestCoreConfigs(TestCase):
    def test_masking_config(self):
        config_dict = {
            'mask_value': 0.
        }
        config = MaskingConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_dropout_config(dropout_class, dim):
        config_dict = {
            'rate': 0.,
            'noise_shape': [1, 1],
            'seed': None
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = dropout_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_dropout_config(self):
        self.assert_dropout_config(DropoutConfig, 1)
        self.assert_dropout_config(SpatialDropout1DConfig, 1)
        self.assert_dropout_config(SpatialDropout2DConfig, 2)
        self.assert_dropout_config(SpatialDropout3DConfig, 3)

    def test_activation_config(self):
        config_dict = {
            'activation': 'relu',
        }
        config = ActivationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_reshape_config(self):
        config_dict = {
            'target_shape': [1, 1]
        }
        config = ReshapeConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_permute_config(self):
        config_dict = {
            'dims': [1, 1]
        }
        config = PermuteConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_flatten_config(self):
        config_dict = {}
        config = FlattenConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_repeat_vector_config(self):
        config_dict = {
            'n': 12,
        }
        config = RepeatVectorConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_dense_config(self):
        config_dict = {
            'units': 12,
            'activation': 'elu',
            'use_bias': True,
            'kernel_initializer': GlorotNormalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'kernel_regularizer': None,
            'bias_regularizer': None,
            'activity_regularizer': None,
            'kernel_constraint': None,
            'bias_constraint': None,
            'inbound_nodes': [['layer_1', 0, 1], ['layer_2', 1, 1]]
        }
        config = DenseConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_activity_regularization_config(self):
        config_dict = {
            'l1': 0.2,
            'l2': 0.32,
        }
        config = ActivityRegularizationConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_cast_config(self):
        config_dict = {
            'dtype': 'float32',
        }
        config = CastConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
