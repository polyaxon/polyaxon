# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import convolutional_recurrent

from polyaxon_schemas.layers.convolutional_recurrent import ConvRecurrent2DConfig, ConvLSTM2DConfig

from polyaxon.libs.base_object import BaseObject
from polyaxon.libs import getters


class ConvRecurrent2D(BaseObject, convolutional_recurrent.ConvRecurrent2D):
    CONFIG = ConvRecurrent2DConfig
    __doc__ = convolutional_recurrent.ConvRecurrent2D.__doc__


class ConvLSTM2D(BaseObject, convolutional_recurrent.ConvLSTM2D):
    CONFIG = ConvLSTM2DConfig
    __doc__ = convolutional_recurrent.ConvLSTM2D.__doc__

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
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
                 return_sequences=False,
                 go_backwards=False,
                 stateful=False,
                 dropout=0.,
                 recurrent_dropout=0.,
                 **kwargs):
        super(ConvLSTM2D, self).__init__(
            filters,
            kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
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
            kernel_constraint=getters.get_regularizer(kernel_constraint),
            recurrent_constraint=getters.get_regularizer(recurrent_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            return_sequences=return_sequences,
            go_backwards=go_backwards,
            stateful=stateful,
            dropout=dropout,
            recurrent_dropout=recurrent_dropout,
            **kwargs)


CONVOLUTIONAL_RECURRENT_LAYERS = OrderedDict([
    (ConvRecurrent2D.CONFIG.IDENTIFIER, ConvRecurrent2D),
    (ConvLSTM2D.CONFIG.IDENTIFIER, ConvLSTM2D),
])
