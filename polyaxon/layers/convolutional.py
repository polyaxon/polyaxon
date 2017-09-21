# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import convolutional

from polyaxon_schemas.layers.convolutional import (
    Conv1DConfig,
    Conv2DConfig,
    Conv3DConfig,
    Conv2DTransposeConfig,
    Conv3DTransposeConfig,
    SeparableConv2DConfig,
    UpSampling1DConfig,
    UpSampling2DConfig,
    UpSampling3DConfig,
    ZeroPadding1DConfig,
    ZeroPadding2DConfig,
    ZeroPadding3DConfig,
    Cropping1DConfig,
    Cropping2DConfig,
    Cropping3DConfig,
)

from polyaxon.libs.base_object import BaseObject
from polyaxon.libs import getters


class Conv1D(BaseObject, convolutional.Conv1D):
    CONFIG = Conv1DConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 padding='valid',
                 dilation_rate=1,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv1D, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format='channels_last',
            dilation_rate=dilation_rate,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class Conv2D(BaseObject, convolutional.Conv2D):
    CONFIG = Conv2DConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2D, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
            activation=getters.get_activation(activation) if activation else activation,
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class Conv3D(BaseObject, convolutional.Conv3D):
    CONFIG = Conv3DConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3D, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            dilation_rate=dilation_rate,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class Conv2DTranspose(BaseObject, convolutional.Conv2DTranspose):
    CONFIG = Conv2DTransposeConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2DTranspose, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class Conv3DTranspose(BaseObject, convolutional.Conv3DTranspose):
    CONFIG = Conv3DTransposeConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3DTranspose, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            kernel_initializer=getters.get_initializer(kernel_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            kernel_regularizer=getters.get_regularizer(kernel_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            kernel_constraint=getters.get_constraint(kernel_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class SeparableConv2D(BaseObject, convolutional.SeparableConv2D):
    CONFIG = SeparableConv2DConfig

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 depth_multiplier=1,
                 activation=None,
                 use_bias=True,
                 depthwise_initializer='glorot_uniform',
                 pointwise_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 depthwise_regularizer=None,
                 pointwise_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 depthwise_constraint=None,
                 pointwise_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(SeparableConv2D, self).__init__(
            filters=filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            data_format=data_format,
            depth_multiplier=depth_multiplier,
            activation=getters.get_activation(activation),
            use_bias=use_bias,
            depthwise_initializer=getters.get_initializer(depthwise_initializer),
            pointwise_initializer=getters.get_initializer(pointwise_initializer),
            bias_initializer=getters.get_initializer(bias_initializer),
            depthwise_regularizer=getters.get_regularizer(depthwise_regularizer),
            pointwise_regularizer=getters.get_regularizer(pointwise_regularizer),
            bias_regularizer=getters.get_regularizer(bias_regularizer),
            activity_regularizer=getters.get_regularizer(activity_regularizer),
            depthwise_constraint=getters.get_constraint(depthwise_constraint),
            pointwise_constraint=getters.get_constraint(pointwise_constraint),
            bias_constraint=getters.get_constraint(bias_constraint),
            **kwargs)


class UpSampling1D(BaseObject, convolutional.UpSampling1D):
    CONFIG = UpSampling1DConfig


class UpSampling2D(BaseObject, convolutional.UpSampling2D):
    CONFIG = UpSampling2DConfig


class UpSampling3D(BaseObject, convolutional.UpSampling3D):
    CONFIG = UpSampling3DConfig


class ZeroPadding1D(BaseObject, convolutional.ZeroPadding1D):
    CONFIG = ZeroPadding1DConfig


class ZeroPadding2D(BaseObject, convolutional.ZeroPadding2D):
    CONFIG = ZeroPadding2DConfig


class ZeroPadding3D(BaseObject, convolutional.ZeroPadding3D):
    CONFIG = ZeroPadding3DConfig


class Cropping1D(BaseObject, convolutional.Cropping1D):
    CONFIG = Cropping1DConfig


class Cropping2D(BaseObject, convolutional.Cropping2D):
    CONFIG = Cropping2DConfig


class Cropping3D(BaseObject, convolutional.Cropping3D):
    CONFIG = Cropping3DConfig


CONVOLUTIONAL_LAYERS = OrderedDict([
    (Conv1D.CONFIG.IDENTIFIER, Conv1D),
    (Conv2D.CONFIG.IDENTIFIER, Conv2D),
    (Conv3D.CONFIG.IDENTIFIER, Conv3D),
    (Conv2DTranspose.CONFIG.IDENTIFIER, Conv2DTranspose),
    (Conv3DTranspose.CONFIG.IDENTIFIER, Conv3DTranspose),
    (SeparableConv2D.CONFIG.IDENTIFIER, SeparableConv2D),
    (UpSampling1D.CONFIG.IDENTIFIER, UpSampling1D),
    (UpSampling2D.CONFIG.IDENTIFIER, UpSampling2D),
    (UpSampling3D.CONFIG.IDENTIFIER, UpSampling3D),
    (ZeroPadding1D.CONFIG.IDENTIFIER, ZeroPadding1D),
    (ZeroPadding2D.CONFIG.IDENTIFIER, ZeroPadding2D),
    (ZeroPadding3D.CONFIG.IDENTIFIER, ZeroPadding3D),
    (Cropping1D.CONFIG.IDENTIFIER, Cropping1D),
    (Cropping2D.CONFIG.IDENTIFIER, Cropping2D),
    (Cropping3D.CONFIG.IDENTIFIER, Cropping3D),
])
