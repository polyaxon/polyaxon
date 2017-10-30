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
    __doc__ = MaskingConfig.__doc__


class Dropout(BaseObject, core.Dropout):
    CONFIG = DropoutConfig
    __doc__ = DropoutConfig.__doc__


class SpatialDropout1D(BaseObject, core.SpatialDropout1D):
    CONFIG = SpatialDropout1DConfig
    __doc__ = SpatialDropout1DConfig.__doc__


class SpatialDropout2D(BaseObject, core.SpatialDropout2D):
    CONFIG = SpatialDropout2DConfig
    __doc__ = SpatialDropout2DConfig.__doc__


class SpatialDropout3D(BaseObject, core.SpatialDropout3D):
    CONFIG = SpatialDropout3DConfig
    __doc__ = SpatialDropout3DConfig.__doc__


class Activation(BaseObject, core.Activation):
    CONFIG = ActivationConfig
    __doc__ = ActivationConfig.__doc__


class Reshape(BaseObject, core.Reshape):
    CONFIG = ReshapeConfig
    __doc__ = ReshapeConfig.__doc__


class Permute(BaseObject, core.Permute):
    CONFIG = PermuteConfig
    __doc__ = PermuteConfig.__doc__


class Flatten(BaseObject, core.Flatten):
    CONFIG = FlattenConfig
    __doc__ = FlattenConfig.__doc__


class RepeatVector(BaseObject, core.RepeatVector):
    CONFIG = RepeatVectorConfig
    __doc__ = RepeatVectorConfig.__doc__


class Dense(BaseObject, core.Dense):
    CONFIG = DenseConfig
    __doc__ = DenseConfig.__doc__

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
    __doc__ = ActivityRegularizationConfig.__doc__


class Cast(BaseObject, Layer):
    """Casts a tensor to a new type.

    The operation casts `x` (in case of `Tensor`) or `x.values`
    (in case of `SparseTensor`) to `dtype`.

    For example:

    ```python
    # tensor `a` is [1.8, 2.2], dtype=tf.float
    >>> tf.cast(a, tf.int32) ==> [1, 2]  # dtype=tf.int32
    ```

    Args:
        x: A `Tensor` or `SparseTensor`.
        dtype: The destination type.
        name: A name for the operation (optional).

    Returns:
        A `Tensor` or `SparseTensor` with same shape as `x`.

    Raises:
        TypeError: If `x` cannot be cast to the `dtype`.
    """
    CONFIG = CastConfig
    __doc__ = CastConfig.__doc__

    def __init__(self, dtype='float32', **kwargs):
        super(Cast, self).__init__(**kwargs)
        self.dtype = dtype

    def call(self, inputs, **kwargs):
        return tf.cast(inputs, self.dtype)


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
    (Dense.CONFIG.IDENTIFIER, Dense),
    (ActivityRegularization.CONFIG.IDENTIFIER, ActivityRegularization),
    (Cast.CONFIG.IDENTIFIER, Cast),
])
