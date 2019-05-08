# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.fields import ObjectOrListObject, StrOrFct
from polyaxon_schemas.ml.initializations import (
    GlorotUniformInitializerConfig,
    InitializerSchema,
    ZerosInitializerConfig
)
from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.ml.regularizations import RegularizerSchema
from polyaxon_schemas.ml.utils import ACTIVATION_VALUES


class LocallyConnected1DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=1, max=1)
    strides = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)

    @staticmethod
    def schema_config():
        return LocallyConnected1DConfig


class LocallyConnected1DConfig(BaseLayerConfig):
    """Locally-connected layer for 1D inputs.

    The `LocallyConnected1D` layer works similarly to
    the `Conv1D` layer, except that weights are unshared,
    that is, a different set of filters is applied at each different patch
    of the input.

    Example:

    ```python
    # apply a unshared weight convolution 1d of length 3 to a sequence with
    # 10 timesteps, with 64 output filters
    x = LocallyConnected1D(64, 3)(x)
    # now x.output_shape == (None, 8, 64)
    # add a new conv1d on top
    x = LocallyConnected1D(32, 3)(x)
    # now x.output_shape == (None, 6, 32)
    ```

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of a single integer,
            specifying the length of the 1D convolution window.
        strides: An integer or tuple/list of a single integer,
            specifying the stride length of the convolution.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: Currently only supports `"valid"` (case-insensitive).
            `"same"` may be supported in the future.
        activation: Activation function to use.
            If you don't specify anything, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix.
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to the kernel matrix.
        bias_constraint: Constraint function applied to the bias vector.

    Input shape:
        3D tensor with shape: `(batch_size, steps, input_dim)`

    Output shape:
        3D tensor with shape: `(batch_size, new_steps, filters)`
        `steps` value might have changed due to padding or strides.

    Polyaxonfile usage:

    ```yaml
    LocallyConnected1D:
      filters: 64
      kernel_size: 32
    ```
    """
    IDENTIFIER = 'LocallyConnected1D'
    SCHEMA = LocallyConnected1DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(LocallyConnected1DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class LocallyConnected2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    bias_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    kernel_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    activity_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    kernel_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)
    bias_constraint = fields.Nested(RegularizerSchema, default=None, missing=None)

    @staticmethod
    def schema_config():
        return LocallyConnected2DConfig


class LocallyConnected2DConfig(BaseLayerConfig):
    """Locally-connected layer for 2D inputs.

    The `LocallyConnected2D` layer works similarly
    to the `Conv2D` layer, except that weights are unshared,
    that is, a different set of filters is applied at each
    different patch of the input.

    Examples:

    ```python
    # apply a 3x3 unshared weights convolution with 64 output filters on a
    32x32 image
    # with `data_format="channels_last"`:
    x = LocallyConnected2D(64, (3, 3))(x)
    # now X.output_shape == (None, 30, 30, 64)
    # notice that this layer will consume (30*30)*(3*3*3*64) + (30*30)*64
    parameters

    # add a 3x3 unshared weights convolution on top, with 32 output filters:
    x = LocallyConnected2D(32, (3, 3))(x)
    # now x.output_shape == (None, 28, 28, 32)
    ```

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the
            width and height of the 2D convolution window.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        strides: An integer or tuple/list of 2 integers,
            specifying the strides of the convolution along the width and height.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        padding: Currently only support `"valid"` (case-insensitive).
            `"same"` will be supported in future.
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".
        activation: Activation function to use.
            If you don't specify anything, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix.
        bias_initializer: Initializer for the bias vector.
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        kernel_constraint: Constraint function applied to the kernel matrix.
        bias_constraint: Constraint function applied to the bias vector.

    Input shape:
        4D tensor with shape:
        `(samples, channels, rows, cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(samples, rows, cols, channels)` if data_format='channels_last'.

    Output shape:
        4D tensor with shape:
        `(samples, filters, new_rows, new_cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(samples, new_rows, new_cols, filters)` if data_format='channels_last'.
        `rows` and `cols` values might have changed due to padding.

    Polyaxonfile usage:

    ```yaml
    LocallyConnected2D:
      filters: 32
      kernel_size: 3 or [3, 3]
    ```
    """
    IDENTIFIER = 'LocallyConnected2D'
    SCHEMA = LocallyConnected2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotUniformInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(LocallyConnected2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint
