# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf

from tensorflow.contrib.keras.python.keras.engine import Layer
from tensorflow.contrib.keras.python.keras.layers import core

from polyaxon_schemas.layers.core import (
    MaskingConfig,
    DropoutConfig,
    SpatialDropout1DConfig,
    SpatialDropout2DConfig,
    SpatialDropout3DConfig,
    ActivationConfig,
    ReshapeConfig,
    PermuteConfig,
    FlattenConfig,
    RepeatVectorConfig,
    DenseConfig,
    ActivityRegularizationConfig,
    CastConfig,
)

from polyaxon.libs.base_object import BaseObject
from polyaxon.libs import getters


class Masking(BaseObject, core.Masking):
    CONFIG = MaskingConfig


class Dropout(BaseObject, core.Dropout):
    CONFIG = DropoutConfig


class SpatialDropout1D(BaseObject, core.SpatialDropout1D):
    CONFIG = SpatialDropout1DConfig


class SpatialDropout2D(BaseObject, core.SpatialDropout2D):
    CONFIG = SpatialDropout2DConfig


class SpatialDropout3D(BaseObject, core.SpatialDropout3D):
    CONFIG = SpatialDropout3DConfig


class Activation(BaseObject, core.Activation):
    CONFIG = ActivationConfig


class Reshape(BaseObject, core.Reshape):
    CONFIG = ReshapeConfig


class Permute(BaseObject, core.Permute):
    CONFIG = PermuteConfig


class Flatten(BaseObject, core.Flatten):
    CONFIG = FlattenConfig


class RepeatVector(BaseObject, core.RepeatVector):
    CONFIG = RepeatVectorConfig


class Dense(BaseObject, core.Dense):
    CONFIG = DenseConfig

    def __init__(self,
                 units,
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
        super(Dense, self).__init__(
            units,
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


class ActivityRegularization(BaseObject, core.ActivityRegularization):
    CONFIG = ActivityRegularizationConfig


class Cast(BaseObject, Layer):
    CONFIG = CastConfig

    def __init__(self, dtype='float32', **kwargs):
        super(Cast, self).__init__(**kwargs)
        self.dtype = dtype

    def call(self, inputs, **kwargs):
        return tf.cast(inputs, self.dtype)


class Lambda(core.Lambda):
    pass

CORE_LAYERS = OrderedDict([
    (Masking.CONFIG.IDENTIFIER, Masking),
    (Dropout.CONFIG.IDENTIFIER, Dropout),
    (SpatialDropout1D.CONFIG.IDENTIFIER, SpatialDropout1D),
    (SpatialDropout2D.CONFIG.IDENTIFIER, SpatialDropout2D),
    (SpatialDropout3D.CONFIG.IDENTIFIER, SpatialDropout3D),
    (Activation.CONFIG.IDENTIFIER, Activation),
    (Reshape.CONFIG.IDENTIFIER, Reshape),
    (Permute.CONFIG.IDENTIFIER, Permute),
    (Flatten.CONFIG.IDENTIFIER, Flatten),
    (RepeatVector.CONFIG.IDENTIFIER, RepeatVector),
    ('Lambda', core.Lambda),
    (Dense.CONFIG.IDENTIFIER, Dense),
    (ActivityRegularization.CONFIG.IDENTIFIER, ActivityRegularization),
    (Cast.CONFIG.IDENTIFIER, Cast),
])
