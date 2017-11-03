# .CONFIG.IDENTIFIER*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

try:
    from tensorflow.python.keras._impl.keras.layers import recurrent
except ImportError:
    from tensorflow.contrib.keras.python.keras.layers import recurrent

from polyaxon_schemas.layers.recurrent import (
    RecurrentConfig,
    SimpleRNNConfig,
    GRUConfig,
    LSTMConfig,
)

from polyaxon.libs import getters
from polyaxon.libs.base_object import BaseObject


class Recurrent(BaseObject, recurrent.Recurrent):
    CONFIG = RecurrentConfig
    __doc__ = RecurrentConfig.__doc__


class SimpleRNN(BaseObject, recurrent.SimpleRNN):
    CONFIG = SimpleRNNConfig
    __doc__ = SimpleRNNConfig.__doc__

    def __init__(self,
                 units,
                 activation='tanh',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(SimpleRNN, self).__init__(
            units=units,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            recurrent_initializer=getters.get_initializer(recurrent_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            recurrent_regularizer=getters.get_regularizer(recurrent_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            recurrent_constraint=getters.get_constraint(recurrent_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            dropout=dropout,
            recurrent_dropout=recurrent_dropout,
            **kwargs)


class GRU(BaseObject, recurrent.GRU):
    CONFIG = GRUConfig
    __doc__ = GRUConfig.__doc__

    def __init__(self,
                 units,
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(GRU, self).__init__(
            units=units,
            activation=getters.get_activation(activation),
            recurrent_activation=getters.get_activation(recurrent_activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            recurrent_initializer=getters.get_initializer(recurrent_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            recurrent_regularizer=getters.get_regularizer(recurrent_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            recurrent_constraint=getters.get_constraint(recurrent_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            dropout=dropout,
            recurrent_dropout=recurrent_dropout,
            **kwargs)


class LSTM(BaseObject, recurrent.LSTM):
    CONFIG = LSTMConfig
    __doc__ = LSTMConfig.__doc__

    def __init__(self,
                 units,
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 unit_forget_bias=True,
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(LSTM, self).__init__(
            units=units,
            activation=getters.get_activation(activation),
            recurrent_activation=getters.get_activation(recurrent_activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            recurrent_initializer=getters.get_initializer(recurrent_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            unit_forget_bias=unit_forget_bias,
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            recurrent_regularizer=getters.get_regularizer(recurrent_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            recurrent_constraint=getters.get_constraint(recurrent_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            dropout=dropout,
            recurrent_dropout=recurrent_dropout,
            **kwargs)


RECURRENT_LAYERS = OrderedDict([
    (Recurrent.CONFIG.IDENTIFIER, Recurrent),
    (SimpleRNN.CONFIG.IDENTIFIER, SimpleRNN),
    (GRU.CONFIG.IDENTIFIER, GRU),
    (LSTM.CONFIG.IDENTIFIER, LSTM),
])
