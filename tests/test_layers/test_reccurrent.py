# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.initializations import (
    GlorotUniformInitializerConfig,
    OrthogonalInitializerConfig,
    ZerosInitializerConfig
)
from polyaxon_schemas.layers.recurrent import (
    GRUConfig,
    LSTMConfig,
    RecurrentConfig,
    SimpleRNNConfig
)


class TestRecurrentConfigs(TestCase):
    def test_recurrent_config(self):
        config_dict = {
            'return_sequences': False,
            'return_state': False,
            'go_backwards': False,
            'stateful': False,
            'unroll': False,
            'implementation': 0,
        }
        config = RecurrentConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_simple_rnn_config(self):
        config_dict = {
            'units': 3,
            'activation': 'tanh',
            'use_bias': True,
            'kernel_initializer': GlorotUniformInitializerConfig().to_schema(),
            'recurrent_initializer': OrthogonalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'kernel_regularizer': None,
            'recurrent_regularizer': None,
            'bias_regularizer': None,
            'activity_regularizer': None,
            'kernel_constraint': None,
            'recurrent_constraint': None,
            'bias_constraint': None,
            'dropout': 0.,
            'recurrent_dropout': 0.,
        }
        config = SimpleRNNConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_gru_config(self):
        config_dict = {
            'units': 3,
            'activation': 'tanh',
            'recurrent_activation': 'hard_sigmoid',
            'use_bias': True,
            'kernel_initializer': GlorotUniformInitializerConfig().to_schema(),
            'recurrent_initializer': OrthogonalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'kernel_regularizer': None,
            'recurrent_regularizer': None,
            'bias_regularizer': None,
            'activity_regularizer': None,
            'kernel_constraint': None,
            'recurrent_constraint': None,
            'bias_constraint': None,
            'dropout': 0.,
            'recurrent_dropout': 0.,
        }
        config = GRUConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_lstm_config(self):
        config_dict = {
            'units': 3,
            'activation': 'tanh',
            'recurrent_activation': 'hard_sigmoid',
            'use_bias': True,
            'kernel_initializer': GlorotUniformInitializerConfig().to_schema(),
            'recurrent_initializer': OrthogonalInitializerConfig().to_schema(),
            'bias_initializer': ZerosInitializerConfig().to_schema(),
            'unit_forget_bias': True,
            'kernel_regularizer': None,
            'recurrent_regularizer': None,
            'bias_regularizer': None,
            'activity_regularizer': None,
            'kernel_constraint': None,
            'recurrent_constraint': None,
            'bias_constraint': None,
            'dropout': 0.,
            'recurrent_dropout': 0.,
        }
        config = LSTMConfig.from_dict(config_dict)
        assert_equal_layers(config, config_dict)
