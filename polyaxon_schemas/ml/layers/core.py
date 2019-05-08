# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.fields import StrOrFct
from polyaxon_schemas.ml.constraints import ConstraintSchema
from polyaxon_schemas.ml.fields import DType
from polyaxon_schemas.ml.initializations import (
    GlorotNormalInitializerConfig,
    InitializerSchema,
    ZerosInitializerConfig
)
from polyaxon_schemas.ml.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.ml.regularizations import RegularizerSchema
from polyaxon_schemas.ml.utils import ACTIVATION_VALUES


class MaskingSchema(BaseLayerSchema):
    mask_value = fields.Int()

    @staticmethod
    def schema_config():
        return MaskingConfig


class MaskingConfig(BaseLayerConfig):
    """Masks a sequence by using a mask value to skip timesteps.

    For each timestep in the input tensor (dimension #1 in the tensor),
    if all values in the input tensor at that timestep
    are equal to `mask_value`, then the timestep will be masked (skipped)
    in all downstream layers (as long as they support masking).

    If any downstream layer does not support masking yet receives such
    an input mask, an exception will be raised.

    Example:

    Consider a Numpy data array `x` of shape `(samples, timesteps, features)`,
    to be fed to a LSTM layer.
    You want to mask timestep #3 and #5 because you lack data for
    these timesteps. You can:

        - set `x[:, 3, :] = 0.` and `x[:, 5, :] = 0.`
        - insert a `Masking` layer with `mask_value=0.` before the LSTM layer:

    ```python
    x = Masking(mask_value=0., input_shape=(timesteps, features))(x)
    x = LSTM(32)(x)
    ```

    Polyaxonfile usage:

    ```yaml
    Masking:
      mask_value: 0
    ```
    """
    IDENTIFIER = 'Masking'
    SCHEMA = MaskingSchema

    def __init__(self, mask_value=0., **kwargs):
        super(MaskingConfig, self).__init__(**kwargs)
        self.mask_value = mask_value


class DropoutSchema(BaseLayerSchema):
    rate = fields.Float(validate=validate.Range(0, 1))
    noise_shape = fields.List(fields.Int(), default=None, missing=None)
    seed = fields.Int(default=None, missing=None)

    @staticmethod
    def schema_config():
        return DropoutConfig


class DropoutConfig(BaseLayerConfig):
    """Applies Dropout to the input.

    Dropout consists in randomly setting
    a fraction `rate` of input units to 0 at each update during training time,
    which helps prevent overfitting.

    Args:
        rate: float between 0 and 1. Fraction of the input units to drop.
        noise_shape: 1D integer tensor representing the shape of the
            binary dropout mask that will be multiplied with the input.
            For instance, if your inputs have shape
            `(batch_size, timesteps, features)` and
            you want the dropout mask to be the same for all timesteps,
            you can use `noise_shape=(batch_size, 1, features)`.
        seed: A Python integer to use as random seed.

    Polyaxonfile usage:

    ```yaml
    Dropout:
      rate: 0.5
    ```
    """
    IDENTIFIER = 'Dropout'
    SCHEMA = DropoutSchema

    def __init__(self, rate, noise_shape=None, seed=None, **kwargs):
        super(DropoutConfig, self).__init__(**kwargs)
        self.rate = rate
        self.noise_shape = noise_shape
        self.seed = seed


class SpatialDropout1DSchema(DropoutSchema):

    @staticmethod
    def schema_config():
        return SpatialDropout1DConfig


class SpatialDropout1DConfig(DropoutConfig):
    """Spatial 1D version of Dropout.

    This version performs the same function as Dropout, however it drops
    entire 1D feature maps instead of individual elements. If adjacent frames
    within feature maps are strongly correlated (as is normally the case in
    early convolution layers) then regular dropout will not regularize the
    activations and will otherwise just result in an effective learning rate
    decrease. In this case, SpatialDropout1D will help promote independence
    between feature maps and should be used instead.

    Args:
        rate: float between 0 and 1. Fraction of the input units to drop.

    Input shape:
        3D tensor with shape:
        `(samples, timesteps, channels)`

    Output shape:
        Same as input

    References:
        - [Efficient Object Localization Using Convolutional
          Networks](https://arxiv.org/abs/1411.4280)

    Polyaxonfile usage:

    ```yaml
    SpatialDropout1D:
      rate: 0.5
    ```
    """
    IDENTIFIER = 'SpatialDropout1D'
    SCHEMA = SpatialDropout1DSchema


class SpatialDropout2DSchema(DropoutSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return SpatialDropout2DConfig


class SpatialDropout2DConfig(DropoutConfig):
    """Spatial 2D version of Dropout.

    This version performs the same function as Dropout, however it drops
    entire 2D feature maps instead of individual elements. If adjacent pixels
    within feature maps are strongly correlated (as is normally the case in
    early convolution layers) then regular dropout will not regularize the
    activations and will otherwise just result in an effective learning rate
    decrease. In this case, SpatialDropout2D will help promote independence
    between feature maps and should be used instead.

    Args:
        rate: float between 0 and 1. Fraction of the input units to drop.
        data_format: 'channels_first' or 'channels_last'.
            In 'channels_first' mode, the channels dimension
            (the depth) is at index 1,
            in 'channels_last' mode is it at index 3.
            If you never set it, then it will be "channels_last".

    Input shape:
        4D tensor with shape:
        `(samples, channels, rows, cols)` if data_format='channels_first'
        or 4D tensor with shape:
        `(samples, rows, cols, channels)` if data_format='channels_last'.

    Output shape:
        Same as input

    References:
        - [Efficient Object Localization Using Convolutional
          Networks](https://arxiv.org/abs/1411.4280)

    Polyaxonfile usage:

    ```yaml
    SpatialDropout2D:
      rate: 0.5
    ```
    """
    IDENTIFIER = 'SpatialDropout2D'
    SCHEMA = SpatialDropout2DSchema

    def __init__(self, rate, data_format=None, **kwargs):
        super(SpatialDropout2DConfig, self).__init__(rate, **kwargs)
        self.data_format = data_format


class SpatialDropout3DSchema(DropoutSchema):
    data_format = fields.Str(default=None, missing=None,
                             validate=validate.OneOf('channels_first', 'channels_last'))

    @staticmethod
    def schema_config():
        return SpatialDropout3DConfig


class SpatialDropout3DConfig(DropoutConfig):
    """Spatial 3D version of Dropout.

    This version performs the same function as Dropout, however it drops
    entire 3D feature maps instead of individual elements. If adjacent voxels
    within feature maps are strongly correlated (as is normally the case in
    early convolution layers) then regular dropout will not regularize the
    activations and will otherwise just result in an effective learning rate
    decrease. In this case, SpatialDropout3D will help promote independence
    between feature maps and should be used instead.

    Args:
        rate: float between 0 and 1. Fraction of the input units to drop.
        data_format: 'channels_first' or 'channels_last'.
            In 'channels_first' mode, the channels dimension (the depth)
            is at index 1, in 'channels_last' mode is it at index 4.
            If you never set it, then it will be "channels_last".

    Input shape:
        5D tensor with shape:
        `(samples, channels, dim1, dim2, dim3)` if data_format='channels_first'
        or 5D tensor with shape:
        `(samples, dim1, dim2, dim3, channels)` if data_format='channels_last'.

    Output shape:
        Same as input

    References:
        - [Efficient Object Localization Using Convolutional
          Networks](https://arxiv.org/abs/1411.4280)

    Polyaxonfile usage:

    ```yaml
    SpatialDropout3D:
      rate: 0.5
    ```
    """
    IDENTIFIER = 'SpatialDropout3D'
    SCHEMA = SpatialDropout3DSchema

    def __init__(self, rate, data_format=None, **kwargs):
        super(SpatialDropout3DConfig, self).__init__(rate, **kwargs)
        self.data_format = data_format


class ActivationSchema(BaseLayerSchema):
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))

    @staticmethod
    def schema_config():
        return ActivationConfig


class ActivationConfig(BaseLayerConfig):
    """Applies an activation function to an output.

    Args:
        activation: name of activation function.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    Polyaxonfile usage:

    ```yaml
    Activation:
      activation: tanh
    ```
    """
    IDENTIFIER = 'Activation'
    SCHEMA = ActivationSchema

    def __init__(self, activation, **kwargs):
        super(ActivationConfig, self).__init__(**kwargs)
        self.activation = activation


class ReshapeSchema(BaseLayerSchema):
    target_shape = fields.List(fields.Int())

    @staticmethod
    def schema_config():
        return ReshapeConfig


class ReshapeConfig(BaseLayerConfig):
    """Reshapes an output to a certain shape.

    Args:
        target_shape: target shape. Tuple of integers,
            does not include the samples dimension (batch size).

    Input shape:
        Arbitrary, although all dimensions in the input shaped must be fixed.
        Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        `(batch_size,) + target_shape`

    Example:

    ```python
    # as first layer in a Sequential model
    x = Reshape((3, 4))(x)
    # now: x.output_shape == (None, 3, 4)
    # note: `None` is the batch dimension

    # also supports shape inference using `-1` as dimension
    x = Reshape((-1, 2, 2))(x)
    # now: x.output_shape == (None, 3, 2, 2)
    ```

    Polyaxonfile usage:

    ```yaml
    Reshape:
      target_shape: [-1, 2, 2]
    ```
    """
    IDENTIFIER = 'Reshape'
    SCHEMA = ReshapeSchema

    def __init__(self, target_shape, **kwargs):
        super(ReshapeConfig, self).__init__(**kwargs)
        self.target_shape = target_shape


class PermuteSchema(BaseLayerSchema):
    dims = fields.List(fields.Int())

    @staticmethod
    def schema_config():
        return PermuteConfig


class PermuteConfig(BaseLayerConfig):
    """Permutes the dimensions of the input according to a given pattern.

    Useful for e.g. connecting RNNs and convnets together.

    Args:
        dims: Tuple of integers. Permutation pattern, does not include the
            samples dimension. Indexing starts at 1.
            For instance, `(2, 1)` permutes the first and second dimension
            of the input.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same as the input shape, but with the dimensions re-ordered according
        to the specified pattern.

    Example:

    ```python
    x = Permute((2, 1), input_shape=(10, 64))(x)
    # now: X.output_shape == (None, 64, 10)
    # note: `None` is the batch dimension
    ```

    Polyaxonfile usage:

    ```yaml
    Reshape:
      target_shape: [-1, 2, 2]
    ```
    """
    IDENTIFIER = 'Permute'
    SCHEMA = PermuteSchema

    def __init__(self, dims, **kwargs):
        super(PermuteConfig, self).__init__(**kwargs)
        self.dims = dims


class FlattenSchema(BaseLayerSchema):
    @staticmethod
    def schema_config():
        return FlattenConfig


class FlattenConfig(BaseLayerConfig):
    """Flattens the input. Does not affect the batch size.

    Example:

    ```python
    x = Convolution2D(64, 3, 3,
                     border_mode='same',
                     input_shape=(3, 32, 32))(x)
    # now: x.output_shape == (None, 64, 32, 32)

    x = Flatten()(x)
    # now: x.output_shape == (None, 65536)
    ```

    Polyaxonfile usage:

    ```yaml
    Flatten:
    ```
    """
    IDENTIFIER = 'Flatten'
    SCHEMA = FlattenSchema


class RepeatVectorSchema(BaseLayerSchema):
    n = fields.Int()

    @staticmethod
    def schema_config():
        return RepeatVectorConfig


class RepeatVectorConfig(BaseLayerConfig):
    """Repeats the input n times.

    Example:

    ```python
    x = Dense(32)(x)
    # now: x.output_shape == (None, 32)
    # note: `None` is the batch dimension

    x = RepeatVector(3)(x)
    # now: x.output_shape == (None, 3, 32)
    ```

    Args:
        n: integer, repetition factor.

    Input shape:
        2D tensor of shape `(num_samples, features)`.

    Output shape:
        3D tensor of shape `(num_samples, n, features)`.

    Polyaxonfile usage:

    ```yaml
    RepeatVector:
      n: 32
    ```
    """
    IDENTIFIER = 'RepeatVector'
    SCHEMA = RepeatVectorSchema

    def __init__(self, n, **kwargs):
        super(RepeatVectorConfig, self).__init__(**kwargs)
        self.n = n


# class LambdaSchema(BaseLayerSchema):


class DenseSchema(BaseLayerSchema):
    units = fields.Int()
    activation = StrOrFct(allow_none=True, validate=validate.OneOf(ACTIVATION_VALUES))
    use_bias = fields.Bool(allow_none=True)
    kernel_initializer = fields.Nested(InitializerSchema, allow_none=True)
    bias_initializer = fields.Nested(InitializerSchema, allow_none=True)
    kernel_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    bias_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    kernel_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    bias_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return DenseConfig


class DenseConfig(BaseLayerConfig):
    """Just your regular densely-connected NN layer.

    `Dense` implements the operation:
    `output = activation(dot(input, kernel) + bias)`
    where `activation` is the element-wise activation function
    passed as the `activation` argument, `kernel` is a weights matrix
    created by the layer, and `bias` is a bias vector created by the layer
    (only applicable if `use_bias` is `True`).

    Note: if the input to the layer has a rank greater than 2, then
    it is flattened prior to the initial dot product with `kernel`.

    Example:

    ```python
    # as first layer in a sequential model:
    x = Dense(32)(x)
    # now the model will take as input arrays of shape (*, 16)
    # and output arrays of shape (*, 32)
    ```

    Args:
        units: Positive integer, dimensionality of the output space.
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
        kernel_constraint: Constraint function applied to
            the `kernel` weights matrix.
        bias_constraint: Constraint function applied to the bias vector.

    Input shape:
        nD tensor with shape: `(batch_size, ..., input_dim)`.
        The most common situation would be
        a 2D input with shape `(batch_size, input_dim)`.

    Output shape:
        nD tensor with shape: `(batch_size, ..., units)`.
        For instance, for a 2D input with shape `(batch_size, input_dim)`,
        the output would have shape `(batch_size, units)`.

    Polyaxonfile usage:

    ```yaml
    Dense:
      units: 32
      activation: sigmoid
    ```
    """
    IDENTIFIER = 'Dense'
    SCHEMA = DenseSchema

    def __init__(self,
                 units,
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
        super(DenseConfig, self).__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constraint = kernel_constraint
        self.bias_constraint = bias_constraint


class ActivityRegularizationSchema(BaseLayerSchema):
    l1 = fields.Float(allow_none=True)
    l2 = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return ActivityRegularizationConfig


class ActivityRegularizationConfig(BaseLayerConfig):
    """Layer that applies an update to the cost function based input activity.

    Args:
        l1: L1 regularization factor (positive float).
        l2: L2 regularization factor (positive float).

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as input.

    Polyaxonfile usage:

    ```yaml
    ActivityRegularization:
      l1: 0.1
      l2: 0.2
    ```
    """
    IDENTIFIER = 'ActivityRegularization'
    SCHEMA = ActivityRegularizationSchema

    def __init__(self, l1=0., l2=0., **kwargs):
        super(ActivityRegularizationConfig, self).__init__(**kwargs)
        self.l1 = l1
        self.l2 = l2


class CastSchema(BaseLayerSchema):
    dtype = DType()

    @staticmethod
    def schema_config():
        return CastConfig


class CastConfig(BaseLayerConfig):
    """Casts a tensor to a new type.

    The operation casts `x` (in case of `Tensor`) or `x.values`
    (in case of `SparseTensor`) to `dtype`.

    For example:

    ```python
    x = tf.constant([1.8, 2.2], dtype=tf.float32)
    x = Cast(dtype=tf.int32)(x)  # [1, 2], dtype=tf.int32
    ```

    Args:
      x: A `Tensor` or `SparseTensor`.
      dtype: The destination type.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` with same shape as `x`.

    Raises:
      TypeError: If `x` cannot be cast to the `dtype`.

    Polyaxonfile usage:

    ```yaml
    Cast:
      dtype: float32
    ```
    """
    IDENTIFIER = 'Cast'
    SCHEMA = CastSchema

    def __init__(self, dtype, **kwargs):
        super(CastConfig, self).__init__(**kwargs)
        self.dtype = dtype
