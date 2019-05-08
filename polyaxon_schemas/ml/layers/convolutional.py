# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.fields import ObjectOrListObject, StrOrFct
from polyaxon_schemas.ml.constraints import ConstraintSchema
from polyaxon_schemas.ml.initializations import (
    GlorotNormalInitializerConfig,
    InitializerSchema,
    ZerosInitializerConfig
)
from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.ml.regularizations import RegularizerSchema
from polyaxon_schemas.ml.utils import ACTIVATION_VALUES

# pylint:disable=too-many-lines


class Conv1DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=1, max=1)
    strides = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    dilation_rate = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return Conv1DConfig


class Conv1DConfig(BaseLayerConfig):
    """1D convolution layer (e.g. temporal convolution).

    This layer creates a convolution kernel that is convolved
    with the layer input over a single spatial (or temporal) dimension
    to produce a tensor of outputs.
    If `use_bias` is True, a bias vector is created and added to the outputs.
    Finally, if `activation` is not `None`,
    it is applied to the outputs as well.

    When using this layer as the first layer in a model,
    provide an `input_shape` argument
    (tuple of integers or `None`, e.g.
    `(10, 128)` for sequences of 10 vectors of 128-dimensional vectors,
    or `(None, 128)` for variable-length sequences of 128-dimensional vectors.

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of a single integer,
            specifying the length of the 1D convolution window.
        strides: An integer or tuple/list of a single integer,
            specifying the stride length of the convolution.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: One of `"valid"`, `"causal"` or `"same"` (case-insensitive).
            `"causal"` results in causal (dilated) convolutions, e.g. output[t]
            does not depend on input[t+1:]. Useful when modeling temporal data
            where the model should not violate the temporal order.
            See [WaveNet: A Generative Model for Raw Audio, section
              2.1](https://arxiv.org/abs/1609.03499).
        dilation_rate: an integer or tuple/list of a single integer, specifying
            the dilation rate to use for dilated convolution.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any `strides` value != 1.
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

    Polyaxon usage:

    ```yaml
    Conv1D:
      filters: 10
      kernel_size: 3
      strides: 1
      padding: same
    ```
    """
    IDENTIFIER = 'Conv1D'
    SCHEMA = Conv1DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=1,
                 padding='valid',
                 dilation_rate=1,
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv1DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return Conv2DConfig


class Conv2DConfig(BaseLayerConfig):
    """2D convolution layer (e.g. spatial convolution over images).

    This layer creates a convolution kernel that is convolved
    with the layer input to produce a tensor of
    outputs. If `use_bias` is True,
    a bias vector is created and added to the outputs. Finally, if
    `activation` is not `None`, it is applied to the outputs as well.

    When using this layer as the first layer in a model,
    provide the keyword argument `input_shape`
    (tuple of integers, does not include the sample axis),
    e.g. `input_shape=(128, 128, 3)` for 128x128 RGB pictures
    in `data_format="channels_last"`.

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
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: an integer or tuple/list of 2 integers, specifying
            the dilation rate to use for dilated convolution.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any stride value != 1.
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
    Conv2D:
      filters: 10
      kernel_size: 8 or [8, 8]
      strides: 2 or [2, 2]
      padding: valid
      activation: tanh
      kernel_initializer: Ones
    ```

    or


    ```yaml
    Conv2D:
      filters: 10
      kernel_size: [8, 8]
      strides: [2, 2]
      padding: valid
      activation: tanh
      kernel_initializer:
        Ones:
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: [8, 8]
      strides: 1
      padding: valid
      activation: tanh
      kernel_initializer:
        Ones: {dtype: float32}
    ```
    """
    IDENTIFIER = 'Conv2D'
    SCHEMA = Conv2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv3DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=3, max=3)
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=3, max=3,
                                       default=(1, 1, 1), missing=(1, 1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return Conv3DConfig


class Conv3DConfig(BaseLayerConfig):
    """3D convolution layer (e.g. spatial convolution over volumes).

    This layer creates a convolution kernel that is convolved
    with the layer input to produce a tensor of
    outputs. If `use_bias` is True,
    a bias vector is created and added to the outputs. Finally, if
    `activation` is not `None`, it is applied to the outputs as well.

    When using this layer as the first layer in a model,
    provide the keyword argument `input_shape`
    (tuple of integers, does not include the sample axis),
    e.g. `input_shape=(128, 128, 128, 1)` for 128x128x128 volumes
    with a single channel,
    in `data_format="channels_last"`.

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number output of filters in the convolution).
        kernel_size: An integer or tuple/list of 3 integers, specifying the
            depth, height and width of the 3D convolution window.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        strides: An integer or tuple/list of 3 integers,
            specifying the strides of the convolution along each spatial
              dimension.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: an integer or tuple/list of 3 integers, specifying
            the dilation rate to use for dilated convolution.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any stride value != 1.
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
        5D tensor with shape:
        `(samples, channels, conv_dim1, conv_dim2, conv_dim3)` if
          data_format='channels_first'
        or 5D tensor with shape:
        `(samples, conv_dim1, conv_dim2, conv_dim3, channels)` if
          data_format='channels_last'.

    Output shape:
        5D tensor with shape:
        `(samples, filters, new_conv_dim1, new_conv_dim2, new_conv_dim3)` if
          data_format='channels_first'
        or 5D tensor with shape:
        `(samples, new_conv_dim1, new_conv_dim2, new_conv_dim3, filters)` if
          data_format='channels_last'.
        `new_conv_dim1`, `new_conv_dim2` and `new_conv_dim3` values might have
         changed due to padding.

    Polyaxonfile usage:

    ```yaml
    Conv3D:
      filters: 10
      kernel_size: 8 or [8, 8, 8]
      strides: 1 or [1, 1, 1]
      padding: valid
      activation: tanh
      kernel_initializer: Ones
    ```
    """
    IDENTIFIER = 'Conv3D'
    SCHEMA = Conv3DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.dilation_rate = dilation_rate
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv2DTransposeSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    dilation_rate = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return Conv2DTransposeConfig


class Conv2DTransposeConfig(BaseLayerConfig):
    """Transposed convolution layer (sometimes called Deconvolution).

    The need for transposed convolutions generally arises
    from the desire to use a transformation going in the opposite direction
    of a normal convolution, i.e., from something that has the shape of the
    output of some convolution to something that has the shape of its input
    while maintaining a connectivity pattern that is compatible with
    said convolution.

    When using this layer as the first layer in a model,
    provide the keyword argument `input_shape`
    (tuple of integers, does not include the sample axis),
    e.g. `input_shape=(128, 128, 3)` for 128x128 RGB pictures
    in `data_format="channels_last"`.

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number of output filters in the convolution).
        kernel_size: An integer or tuple/list of 2 integers, specifying the
            width and height of the 2D convolution window.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        strides: An integer or tuple/list of 2 integers,
            specifying the strides of the convolution along the width and height.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: an integer or tuple/list of 2 integers, specifying
            the dilation rate to use for dilated convolution.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any stride value != 1.
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
        `(batch, channels, rows, cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(batch, rows, cols, channels)` if data_format='channels_last'.

    Output shape:
        4D tensor with shape:
        `(batch, filters, new_rows, new_cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(batch, new_rows, new_cols, filters)` if data_format='channels_last'.
        `rows` and `cols` values might have changed due to padding.

    References:
        - [A guide to convolution arithmetic for deep
          learning](https://arxiv.org/abs/1603.07285v1)
        - [Deconvolutional
          Networks](http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf)

    Polyaxonfile usage:

    ```yaml
    Conv2DTranspose:
      filters: 10
      kernel_soze: [4, 4]
    ```
    """
    IDENTIFIER = 'Conv2DTranspose'
    SCHEMA = Conv2DTransposeSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 dilation_rate=(1, 1),
                 activation=None,
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv2DTransposeConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.dilation_rate = dilation_rate
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class Conv3DTransposeSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=3, max=3)
    strides = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    dilation_rate = ObjectOrListObject(fields.Int, min=3, max=3,
                                       default=(1, 1, 1), missing=(1, 1, 1))
    use_bias = fields.Bool(default=True, missing=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return Conv3DTransposeConfig


class Conv3DTransposeConfig(BaseLayerConfig):
    """Transposed convolution layer (sometimes called Deconvolution).

    The need for transposed convolutions generally arises
    from the desire to use a transformation going in the opposite direction
    of a normal convolution, i.e., from something that has the shape of the
    output of some convolution to something that has the shape of its input
    while maintaining a connectivity pattern that is compatible with
    said convolution.

    When using this layer as the first layer in a model,
    provide the keyword argument `input_shape`
    (tuple of integers, does not include the sample axis),
    e.g. `input_shape=(128, 128, 128, 3)` for a 128x128x128 volume with 3 channels
    if `data_format="channels_last"`.

    Args:
        filters: Integer, the dimensionality of the output space
            (i.e. the number of output filters in the convolution).
        kernel_size: An integer or tuple/list of 3 integers, specifying the
            depth, height and width of the 3D convolution window.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        strides: An integer or tuple/list of 3 integers,
            specifying the strides of the convolution along the depth, height
              and width.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, depth, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, depth, height, width)`.
            If you never set it, then it will be "channels_last".
        dilation_rate: an integer or tuple/list of 3 integers, specifying
            the dilation rate to use for dilated convolution.
            Can be a single integer to specify the same value for
            all spatial dimensions.
            Currently, specifying any `dilation_rate` value != 1 is
            incompatible with specifying any stride value != 1.
        activation: Activation function to use
            If you don't specify anything, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        use_bias: Boolean, whether the layer uses a bias vector.
        kernel_initializer: Initializer for the `kernel` weights matrix
        bias_initializer: Initializer for the bias vector
        kernel_regularizer: Regularizer function applied to
            the `kernel` weights matrix
        bias_regularizer: Regularizer function applied to the bias vector
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation").
        kernel_constraint: Constraint function applied to the kernel matrix
        bias_constraint: Constraint function applied to the bias vector

    Input shape:
        5D tensor with shape:
        `(batch, channels, depth, rows, cols)` if data_format='channels_first'
        or 5D tensor with shape:
        `(batch, depth, rows, cols, channels)` if data_format='channels_last'.

    Output shape:
        5D tensor with shape:
        `(batch, filters, new_depth, new_rows, new_cols)` if
          data_format='channels_first'
        or 5D tensor with shape:
        `(batch, new_depth, new_rows, new_cols, filters)` if
          data_format='channels_last'.
        `depth` and `rows` and `cols` values might have changed due to padding.

    References:
        - [A guide to convolution arithmetic for deep
          learning](https://arxiv.org/abs/1603.07285v1)
        - [Deconvolutional
          Networks](http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf)

    Polyaxonfile usage:

    ```yaml
    Conv3DTranspose:
      filters: 10
      kernel_size: 3 or [3, 3, 3]
    ```
    """
    IDENTIFIER = 'Conv3DTranspose'
    SCHEMA = Conv3DTransposeSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1, 1),
                 padding='valid',
                 data_format=None,
                 activation=None,
                 dilation_rate=(1, 1, 1),
                 use_bias=True,
                 kernel_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(Conv3DTransposeConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.activation = activation
        self.dilation_rate = dilation_rate
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class SeparableConv2DSchema(BaseLayerSchema):
    filters = fields.Int()
    kernel_size = ObjectOrListObject(fields.Int, min=2, max=2)
    strides = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    padding = fields.Str(default='valid', missing='valid',
                         validate=validate.OneOf(['same', 'valid']))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))
    depth_multiplier = fields.Int(default=1, missing=1)
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(default=True, missing=True)
    depthwise_initializer = fields.Nested(InitializerSchema, allow_none=True)
    pointwise_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    depthwise_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    pointwise_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    depthwise_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    pointwise_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return SeparableConv2DConfig


class SeparableConv2DConfig(BaseLayerConfig):
    """Depthwise separable 2D convolution.

    Separable convolutions consist in first performing
    a depthwise spatial convolution
    (which acts on each input channel separately)
    followed by a pointwise convolution which mixes together the resulting
    output channels. The `depth_multiplier` argument controls how many
    output channels are generated per input channel in the depthwise step.

    Intuitively, separable convolutions can be understood as
    a way to factorize a convolution kernel into two smaller kernels,
    or as an extreme version of an Inception block.

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
            Specifying any stride value != 1 is incompatible with specifying
            any `dilation_rate` value != 1.
        padding: one of `"valid"` or `"same"` (case-insensitive).
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".
        depth_multiplier: The number of depthwise convolution output channels
            for each input channel.
            The total number of depthwise convolution output
            channels will be equal to `filterss_in * depth_multiplier`.
        activation: Activation function to use.
            If you don't specify anything, no activation is applied
            (ie. "linear" activation: `a(x) = x`).
        use_bias: Boolean, whether the layer uses a bias vector.
        depthwise_initializer: Initializer for the depthwise kernel matrix.
        pointwise_initializer: Initializer for the pointwise kernel matrix.
        bias_initializer: Initializer for the bias vector.
        depthwise_regularizer: Regularizer function applied to
            the depthwise kernel matrix.
        pointwise_regularizer: Regularizer function applied to
            the pointwise kernel matrix.
        bias_regularizer: Regularizer function applied to the bias vector.
        activity_regularizer: Regularizer function applied to
            the output of the layer (its "activation")..
        depthwise_constraint: Constraint function applied to
            the depthwise kernel matrix.
        pointwise_constraint: Constraint function applied to
            the pointwise kernel matrix.
        bias_constraint: Constraint function applied to the bias vector.

    Input shape:
        4D tensor with shape:
        `(batch, channels, rows, cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(batch, rows, cols, channels)` if data_format='channels_last'.

    Output shape:
        4D tensor with shape:
        `(batch, filters, new_rows, new_cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(batch, new_rows, new_cols, filters)` if data_format='channels_last'.
        `rows` and `cols` values might have changed due to padding.

    Polyaxonfile usage:

    ```yaml
    SeparableConv2D:
      filters: 10
      kernel_size: 2 or [2, 2]
    ```
    """
    IDENTIFIER = 'SeparableConv2D'
    SCHEMA = SeparableConv2DSchema

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 data_format=None,
                 depth_multiplier=1,
                 activation=None,
                 use_bias=True,
                 depthwise_initializer=GlorotNormalInitializerConfig(),
                 pointwise_initializer=GlorotNormalInitializerConfig(),
                 bias_initializer=ZerosInitializerConfig(),
                 depthwise_regularizer=None,
                 pointwise_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 depthwise_constraint=None,
                 pointwise_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        super(SeparableConv2DConfig, self).__init__(**kwargs)
        self.filters = filters
        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format
        self.depth_multiplier = depth_multiplier
        self.activation = activation
        self.use_bias = use_bias
        self.depthwise_initializer = depthwise_initializer
        self.pointwise_initializer = pointwise_initializer
        self.bias_initializer = bias_initializer
        self.depthwise_regularizer = depthwise_regularizer
        self.pointwise_regularizer = pointwise_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.depthwise_constraint = depthwise_constraint
        self.pointwise_constraint = pointwise_constraint
        self.bias_constraint = bias_constraint


class UpSampling1DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=2, max=2, default=2, missing=2)

    @staticmethod
    def schema_config():
        return UpSampling1DConfig


class UpSampling1DConfig(BaseLayerConfig):
    """Upsampling layer for 1D inputs.

    Repeats each temporal step `size` times along the time axis.

    Args:
        size: integer. Upsampling factor.

    Input shape:
        3D tensor with shape: `(batch, steps, features)`.

    Output shape:
        3D tensor with shape: `(batch, upsampled_steps, features)`.

    Polyaxonfile usage:

    ```yaml
    UpSampling1D:
    ```

    or

    ```yaml
    UpSampling1D:
        size: 2
    ```

    or

    ```yaml
    UpSampling1D: {size: 2}
    ```
    """
    IDENTIFIER = 'UpSampling1D'
    SCHEMA = UpSampling1DSchema

    def __init__(self, size=2, **kwargs):
        super(UpSampling1DConfig, self).__init__(**kwargs)
        self.size = size


class UpSampling2DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=2, max=2, default=(2, 2), missing=(2, 2))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return UpSampling2DConfig


class UpSampling2DConfig(BaseLayerConfig):
    """Upsampling layer for 2D inputs.

    Repeats the rows and columns of the data
    by size[0] and size[1] respectively.

    Args:
        size: int, or tuple of 2 integers.
            The upsampling factors for rows and columns.
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, rows, cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, rows, cols)`

    Output shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, upsampled_rows, upsampled_cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, upsampled_rows, upsampled_cols)`

    Polyaxonfile usage:

    ```yaml
    UpSampling2D:
    ```

    or

    ```yaml
    UpSampling2D:
        size: 2 or [2, 2]
    ```
    """
    IDENTIFIER = 'UpSampling2D'
    SCHEMA = UpSampling2DSchema

    def __init__(self, size=(2, 2), data_format=None, **kwargs):
        super(UpSampling2DConfig, self).__init__(**kwargs)
        self.size = size
        self.data_format = data_format


class UpSampling3DSchema(BaseLayerSchema):
    size = ObjectOrListObject(fields.Int, min=3, max=3, default=(2, 2, 2), missing=(2, 2, 2))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return UpSampling3DConfig


class UpSampling3DConfig(BaseLayerConfig):
    """Upsampling layer for 3D inputs.

    Repeats the 1st, 2nd and 3rd dimensions
    of the data by size[0], size[1] and size[2] respectively.

    Args:
        size: int, or tuple of 3 integers.
            The upsampling factors for dim1, dim2 and dim3.
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, dim1, dim2, dim3, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, dim1, dim2, dim3)`

    Output shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, upsampled_dim1, upsampled_dim2, upsampled_dim3, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, upsampled_dim1, upsampled_dim2, upsampled_dim3)`

    Polyaxonfile usage:

    ```yaml
    UpSampling3D:
    ```

    or

    ```yaml
    UpSampling3D:
        size: 2 or [2, 2, 2]
    ```
    """
    IDENTIFIER = 'UpSampling3D'
    SCHEMA = UpSampling3DSchema

    def __init__(self, size=(2, 2, 2), data_format=None, **kwargs):
        super(UpSampling3DConfig, self).__init__(**kwargs)
        self.size = size
        self.data_format = data_format


class ZeroPadding1DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=1, max=1, default=1, missing=1)

    @staticmethod
    def schema_config():
        return ZeroPadding1DConfig


class ZeroPadding1DConfig(BaseLayerConfig):
    """Zero-padding layer for 1D input (e.g. temporal sequence).

    Args:
        padding: int, or tuple of int (length 2), or dictionary.
            - If int:
            How many zeros to add at the beginning and end of
            the padding dimension (axis 1).
            - If tuple of int (length 2):
            How many zeros to add at the beginning and at the end of
            the padding dimension (`(left_pad, right_pad)`).

    Input shape:
        3D tensor with shape `(batch, axis_to_pad, features)`

    Output shape:
        3D tensor with shape `(batch, padded_axis, features)`

    Polyaxonfile usage:

    ```yaml
    ZeroPadding1D:
    ```

    or

    ```yaml
    ZeroPadding1D:
        padding: 1
    ```
    """
    IDENTIFIER = 'ZeroPadding1D'
    SCHEMA = ZeroPadding1DSchema

    def __init__(self, padding=1, **kwargs):
        super(ZeroPadding1DConfig, self).__init__(**kwargs)
        self.padding = padding


class ZeroPadding2DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return ZeroPadding2DConfig


class ZeroPadding2DConfig(BaseLayerConfig):
    """Zero-padding layer for 2D input (e.g. picture).

    This layer can add rows and columns of zeros
    at the top, bottom, left and right side of an image tensor.

    Args:
        padding: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
            - If int: the same symmetric padding
                is applied to width and height.
            - If tuple of 2 ints:
                interpreted as two different
                symmetric padding values for height and width:
                `(symmetric_height_pad, symmetric_width_pad)`.
            - If tuple of 2 tuples of 2 ints:
                interpreted as
                `((top_pad, bottom_pad), (left_pad, right_pad))`
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, rows, cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, rows, cols)`

    Output shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, padded_rows, padded_cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, padded_rows, padded_cols)`

    Polyaxonfile usage:

    ```yaml
    ZeroPadding2D:
    ```

    or

    ```yaml
    ZeroPadding2D:
        padding: 1 or [1, 1]
    ```
    """
    IDENTIFIER = 'ZeroPadding2D'
    SCHEMA = ZeroPadding2DSchema

    def __init__(self, padding=(1, 1), data_format=None, **kwargs):
        super(ZeroPadding2DConfig, self).__init__(**kwargs)
        self.padding = padding
        self.data_format = data_format


class ZeroPadding3DSchema(BaseLayerSchema):
    padding = ObjectOrListObject(fields.Int, min=3, max=3, default=(1, 1, 1), missing=(1, 1, 1))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return ZeroPadding3DConfig


class ZeroPadding3DConfig(BaseLayerConfig):
    """Zero-padding layer for 3D data (spatial or spatio-temporal).

    Args:
        padding: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
            - If int: the same symmetric padding
                is applied to width and height.
            - If tuple of 2 ints:
                interpreted as two different
                symmetric padding values for height and width:
                `(symmetric_dim1_pad, symmetric_dim2_pad, symmetric_dim3_pad)`.
            - If tuple of 2 tuples of 2 ints:
                interpreted as
                `((left_dim1_pad, right_dim1_pad), (left_dim2_pad,
                  right_dim2_pad), (left_dim3_pad, right_dim3_pad))`
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, first_axis_to_pad, second_axis_to_pad, third_axis_to_pad,
              depth)`
        - If `data_format` is `"channels_first"`:
            `(batch, depth, first_axis_to_pad, second_axis_to_pad,
              third_axis_to_pad)`

    Output shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, first_padded_axis, second_padded_axis, third_axis_to_pad,
              depth)`
        - If `data_format` is `"channels_first"`:
            `(batch, depth, first_padded_axis, second_padded_axis,
              third_axis_to_pad)`

    Polyaxonfile usage:

    ```yaml
    ZeroPadding3D:
    ```

    or

    ```yaml
    ZeroPadding3D:
        padding: 1 or [1, 1, 1]
    ```
    """
    IDENTIFIER = 'ZeroPadding3D'
    SCHEMA = ZeroPadding3DSchema

    def __init__(self, padding=(1, 1, 1), data_format=None, **kwargs):
        super(ZeroPadding3DConfig, self).__init__(**kwargs)
        self.padding = padding
        self.data_format = data_format


class Cropping1DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(fields.Int, min=2, max=2, default=(1, 1), missing=(1, 1))

    @staticmethod
    def schema_config():
        return Cropping1DConfig


class Cropping1DConfig(BaseLayerConfig):
    """Cropping layer for 1D input (e.g. temporal sequence).

    It crops along the time dimension (axis 1).

    Args:
        cropping: int or tuple of int (length 2)
            How many units should be trimmed off at the beginning and end of
            the cropping dimension (axis 1).
            If a single int is provided,
            the same value will be used for both.

    Input shape:
        3D tensor with shape `(batch, axis_to_crop, features)`

    Output shape:
        3D tensor with shape `(batch, cropped_axis, features)`

    Polyaxonfile usage:

    ```yaml
    Cropping1D:
    ```

    or

    ```yaml
    Cropping1D:
        cropping: 1 or [1, 1]
    ```
    """
    IDENTIFIER = 'Cropping1D'
    SCHEMA = Cropping1DSchema

    def __init__(self, cropping=(1, 1), **kwargs):
        super(Cropping1DConfig, self).__init__(**kwargs)
        self.cropping = cropping


class Cropping2DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(ObjectOrListObject(fields.Int, min=2, max=2), min=2, max=2,
                                  default=((0, 0), (0, 0)), missing=((0, 0), (0, 0)))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return Cropping2DConfig


class Cropping2DConfig(BaseLayerConfig):
    """Cropping layer for 2D input (e.g. picture).

    It crops along spatial dimensions, i.e. width and height.

    Args:
        cropping: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
            - If int: the same symmetric cropping
                is applied to width and height.
            - If tuple of 2 ints:
                interpreted as two different
                symmetric cropping values for height and width:
                `(symmetric_height_crop, symmetric_width_crop)`.
            - If tuple of 2 tuples of 2 ints:
                interpreted as
                `((top_crop, bottom_crop), (left_crop, right_crop))`
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, height, width, channels)` while `channels_first`
            corresponds to inputs with shape
            `(batch, channels, height, width)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, rows, cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, rows, cols)`

    Output shape:
        4D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, cropped_rows, cropped_cols, channels)`
        - If `data_format` is `"channels_first"`:
            `(batch, channels, cropped_rows, cropped_cols)`

    Example:

    ```python
    # Crop the input 2D images or feature maps
    x = Cropping2D(cropping=((2, 2), (4, 4)), input_shape=(28, 28, 3))(x)
    # now x.output_shape == (None, 24, 20, 3)
    x = Conv2D(64, (3, 3), padding='same')(x)
    x = Cropping2D(cropping=((2, 2), (2, 2)))(x)
    # now x.output_shape == (None, 20, 16. 64)
    ```

    Polyaxonfile usage:

    ```yaml
    Cropping2D:
      cropping=[[2, 2], [4, 4]]
    ```
    """
    IDENTIFIER = 'Cropping2D'
    SCHEMA = Cropping2DSchema

    def __init__(self, cropping=((0, 0), (0, 0)), data_format=None, **kwargs):
        super(Cropping2DConfig, self).__init__(**kwargs)
        self.cropping = cropping
        self.data_format = data_format


class Cropping3DSchema(BaseLayerSchema):
    cropping = ObjectOrListObject(ObjectOrListObject(fields.Int, min=2, max=2), min=3, max=3,
                                  default=((1, 1), (1, 1), (1, 1)),
                                  missing=((1, 1), (1, 1), (1, 1)))
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return Cropping3DConfig


class Cropping3DConfig(BaseLayerConfig):
    """Cropping layer for 3D data (e.g.

    spatial or spatio-temporal).

    Args:
        cropping: int, or tuple of 23ints, or tuple of 3 tuples of 2 ints.
            - If int: the same symmetric cropping
                is applied to depth, height, and width.
            - If tuple of 3 ints:
                interpreted as two different
                symmetric cropping values for depth, height, and width:
                `(symmetric_dim1_crop, symmetric_dim2_crop, symmetric_dim3_crop)`.
            - If tuple of 3 tuples of 2 ints:
                interpreted as
                `((left_dim1_crop, right_dim1_crop), (left_dim2_crop,
                  right_dim2_crop), (left_dim3_crop, right_dim3_crop))`
        data_format: A string,
            one of `channels_last` (default) or `channels_first`.
            The ordering of the dimensions in the inputs.
            `channels_last` corresponds to inputs with shape
            `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
            while `channels_first` corresponds to inputs with shape
            `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
            If you never set it, then it will be "channels_last".

    Input shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, first_axis_to_crop, second_axis_to_crop, third_axis_to_crop,
              depth)`
        - If `data_format` is `"channels_first"`:
            `(batch, depth, first_axis_to_crop, second_axis_to_crop,
              third_axis_to_crop)`

    Output shape:
        5D tensor with shape:
        - If `data_format` is `"channels_last"`:
            `(batch, first_cropped_axis, second_cropped_axis, third_cropped_axis,
              depth)`
        - If `data_format` is `"channels_first"`:
            `(batch, depth, first_cropped_axis, second_cropped_axis,
              third_cropped_axis)`

    Polyaxonfile usage:

    ```yaml
    Cropping3D:
      cropping=[[2, 2], [4, 4], [2, 2]]
    ```
    """
    IDENTIFIER = 'Cropping3D'
    SCHEMA = Cropping3DSchema

    def __init__(self, cropping=((1, 1), (1, 1), (1, 1)), data_format=None, **kwargs):
        super(Cropping3DConfig, self).__init__(**kwargs)
        self.cropping = cropping
        self.data_format = data_format
