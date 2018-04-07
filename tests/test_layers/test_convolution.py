# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.constraints import MaxNormConfig
from polyaxon_schemas.initializations import GlorotNormalInitializerConfig, ZerosInitializerConfig
from polyaxon_schemas.layers.convolutional import (
    Conv1DConfig,
    Conv2DConfig,
    Conv2DTransposeConfig,
    Conv3DConfig,
    Conv3DTransposeConfig,
    Cropping1DConfig,
    Cropping2DConfig,
    Cropping3DConfig,
    SeparableConv2DConfig,
    UpSampling1DConfig,
    UpSampling2DConfig,
    UpSampling3DConfig,
    ZeroPadding1DConfig,
    ZeroPadding2DConfig,
    ZeroPadding3DConfig
)
from polyaxon_schemas.regularizations import L1L2RegularizerConfig, L1RegularizerConfig


class TestConvolutionConfigs(TestCase):
    @staticmethod
    def assert_conv_config(conv_class, dim):
        config_dict = {
            'filters': 30,
            'kernel_size': 3,
            'strides': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
            'padding': 'valid',
            'activation': 'relu',
            'dilation_rate': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
            'use_bias': True,
            'kernel_initializer': GlorotNormalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'kernel_regularizer': L1L2RegularizerConfig().to_schema(),
            'bias_regularizer': None,
            'activity_regularizer': L1RegularizerConfig().to_schema(),
            'kernel_constraint': MaxNormConfig().to_schema(),
            'bias_constraint': None,
            'inbound_nodes': [['layer_1', 0, 1], ['layer_2', 1, 1]]
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = conv_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_separable_conv(conv_class, dim):
        config_dict = {
            'filters': 30,
            'kernel_size': 10,
            'strides': [1, 1] if dim == 2 else [1, 1, 1],
            'padding': 'valid',
            'data_format': None,
            'depth_multiplier': 1,
            'activation': None,
            'use_bias': True,
            'depthwise_initializer': GlorotNormalInitializerConfig().to_schema(),
            'pointwise_initializer': GlorotNormalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'depthwise_regularizer': None,
            'pointwise_regularizer': None,
            'bias_regularizer': None,
            'activity_regularizer': None,
            'depthwise_constraint': None,
            'pointwise_constraint': None,
            'bias_constraint': None
        }
        config = conv_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_upsampling(upsampling_class, dim):
        config_dict = {
            'size': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = upsampling_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_zero_padding(zero_padding_class, dim):
        config_dict = {
            'padding': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = zero_padding_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_cropping(zero_padding_class, dim):
        config_dict = {
            'cropping': (
                1 if dim == 1 else [[1, 1], [1, 1]]
                if dim == 2 else [[1, 1], [1, 1], [1, 1]]
            ),
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = zero_padding_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_conv_config(self):
        self.assert_conv_config(Conv1DConfig, 1)
        self.assert_conv_config(Conv2DConfig, 2)
        self.assert_conv_config(Conv3DConfig, 3)
        self.assert_conv_config(Conv2DTransposeConfig, 2)
        self.assert_conv_config(Conv3DTransposeConfig, 3)

    def test_separable_conv_config(self):
        self.assert_separable_conv(SeparableConv2DConfig, 2)

    def test_upsampling_config(self):
        self.assert_upsampling(UpSampling1DConfig, 1)
        self.assert_upsampling(UpSampling2DConfig, 2)
        self.assert_upsampling(UpSampling3DConfig, 3)

    def test_zero_padding_config(self):
        self.assert_zero_padding(ZeroPadding1DConfig, 1)
        self.assert_zero_padding(ZeroPadding2DConfig, 2)
        self.assert_zero_padding(ZeroPadding3DConfig, 3)

    def test_cropping_config(self):
        self.assert_cropping(Cropping1DConfig, 1)
        self.assert_cropping(Cropping2DConfig, 2)
        self.assert_cropping(Cropping3DConfig, 3)
