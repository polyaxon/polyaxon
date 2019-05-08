# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema
from polyaxon_schemas.ml.fields import DType

# pylint:disable=too-many-lines


class ZerosInitializerSchema(BaseSchema):
    dtype = DType(allow_none=True)

    @staticmethod
    def schema_config():
        return ZerosInitializerConfig


class ZerosInitializerConfig(BaseConfig):
    """Initializer that generates tensors initialized to 0.

    Args:
        dtype: The data type.

    Returns:
        An initializer.

    Polyaxonfile usage:

    Using the default values

    ```yaml
    Zeros:
    ```

    Using custom values

    ```yaml
    Zeros:
      dtype: int16
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Zeros
    ```
    """
    IDENTIFIER = 'Zeros'
    SCHEMA = ZerosInitializerSchema

    def __init__(self, dtype='float32'):
        self.dtype = dtype


class OnesInitializerSchema(BaseSchema):
    dtype = DType(allow_none=True)

    @staticmethod
    def schema_config():
        return OnesInitializerConfig


class OnesInitializerConfig(BaseConfig):
    """Initializer that generates tensors initialized to 1.

    Args:
        dtype: The data type.

    Returns:
        An initializer.

    Polyaxonfile usage:

    Using the default values

    ```yaml
    Ones:
    ```

    Using custom values

    ```yaml
    Ones:
      dtype: int16
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Ones
    ```
    """
    IDENTIFIER = 'Ones'
    SCHEMA = OnesInitializerSchema

    def __init__(self, dtype='float32'):
        self.dtype = dtype


class ConstantInitializerSchema(BaseSchema):
    value = fields.Int(allow_none=True)
    dtype = DType(allow_none=True)

    @staticmethod
    def schema_config():
        return ConstantInitializerConfig


class ConstantInitializerConfig(BaseConfig):
    """Initializer that generates tensors with constant values.

    The resulting tensor is populated with values of type `dtype`, as
    specified by arguments `value` following the desired `shape` of the
    new tensor (see examples below).

    The argument `value` can be a constant value, or a list of values of type
    `dtype`. If `value` is a list, then the length of the list must be less
    than or equal to the number of elements implied by the desired shape of the
    tensor. In the case where the total number of elements in `value` is less
    than the number of elements required by the tensor shape, the last element
    in `value` will be used to fill the remaining entries. If the total number of
    elements in `value` is greater than the number of elements required by the
    tensor shape, the initializer will raise a `ValueError`.

    Args:
        value: A Python scalar, list of values, or a N-dimensional numpy array. All
            elements of the initialized variable will be set to the corresponding
            value in the `value` argument.
        dtype: The data type.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    Constant:
      value: 3
      dtype: int16
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        Constant:
          value: 3
    ```
    """
    IDENTIFIER = 'Constant'
    SCHEMA = ConstantInitializerSchema

    def __init__(self, value=0, dtype='float32'):
        self.dtype = dtype
        self.value = value


class UniformInitializerSchema(BaseSchema):
    minval = fields.Number(allow_none=True)
    maxval = fields.Number(allow_none=True)
    dtype = DType(allow_none=True)
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return UniformInitializerConfig


class UniformInitializerConfig(BaseConfig):
    """Initializer that generates tensors with a uniform distribution.

    Args:
        minval: A python scalar or a scalar tensor. Lower bound of the range
            of random values to generate.
        maxval: A python scalar or a scalar tensor. Upper bound of the range
            of random values to generate.  Defaults to 1 for float types.
        seed: A Python integer. Used to create random seeds. See
            @{tf.set_random_seed} for behavior.
        dtype: The data type.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    Uniform:
      minval: 1
      maxval: 2
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Uniform
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        Uniform:
          minval: 1
    ```
    """
    IDENTIFIER = 'Uniform'
    SCHEMA = UniformInitializerSchema

    def __init__(self, minval=0, maxval=None, seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.minval = minval
        self.maxval = maxval


class NormalInitializerSchema(BaseSchema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)
    dtype = DType(allow_none=True)
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return NormalInitializerConfig


class NormalInitializerConfig(BaseConfig):
    """Initializer that generates tensors with a normal distribution.

    Args:
        mean: a python scalar or a scalar tensor. Mean of the random values to generate.
        stddev: a python scalar or a scalar tensor. Standard deviation of the
            random values to generate.
        seed: A Python integer. Used to create random seeds. See
            @{tf.set_random_seed} for behavior.
        dtype: The data type. Only floating point types are supported.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    Normal:
      mean: 0.5
      stddev: 1.
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Normal
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        Normal:
          mean: 1.
    ```
    """
    IDENTIFIER = 'Normal'
    SCHEMA = NormalInitializerSchema

    def __init__(self, mean=0., stddev=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.mean = mean
        self.stddev = stddev


class TruncatedNormalInitializerSchema(BaseSchema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)

    @staticmethod
    def schema_config():
        return TruncatedNormalInitializerConfig


class TruncatedNormalInitializerConfig(BaseConfig):
    """Initializer that generates a truncated normal distribution.

    These values are similar to values from a `random_normal_initializer`
    except that values more than two standard deviations from the mean
    are discarded and re-drawn. This is the recommended initializer for
    neural network weights and filters.

    Args:
        mean: a python scalar or a scalar tensor. Mean of the random values to generate.
        stddev: a python scalar or a scalar tensor. Standard deviation of the
            random values to generate.
        seed: A Python integer. Used to create random seeds. See
            @{tf.set_random_seed} for behavior.
        dtype: The data type. Only floating point types are supported.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    TruncatedNormal:
      mean: 0.5
      stddev: 1.
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: TruncatedNormal
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        TruncatedNormal:
          mean: 1.
    ```
    """
    IDENTIFIER = 'TruncatedNormal'
    SCHEMA = TruncatedNormalInitializerSchema

    def __init__(self, mean=0., stddev=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.mean = mean
        self.stddev = stddev


class VarianceScalingInitializerSchema(BaseSchema):
    scale = fields.Float(allow_none=True)
    mode = fields.Str(allow_none=True, validate=validate.OneOf(['fan_in', 'fan_out', 'fan_avg']))
    distribution = fields.Str(allow_none=True)
    dtype = DType(allow_none=True)

    @staticmethod
    def schema_config():
        return VarianceScalingInitializerConfig


class VarianceScalingInitializerConfig(BaseConfig):
    """Initializer capable of adapting its scale to the shape of weights tensors.

    With `distribution="normal"`, samples are drawn from a truncated normal
    distribution centered on zero, with `stddev = sqrt(scale / n)`
    where n is:
      - number of input units in the weight tensor, if mode = "fan_in"
      - number of output units, if mode = "fan_out"
      - average of the numbers of input and output units, if mode = "fan_avg"

    With `distribution="uniform"`, samples are drawn from a uniform distribution
    within [-limit, limit], with `limit = sqrt(3 * scale / n)`.

    Args:
        scale: Scaling factor (positive float).
        mode: One of "fan_in", "fan_out", "fan_avg".
        distribution: Random distribution to use. One of "normal", "uniform".
        seed: A Python integer. Used to create random seeds. See
            @{tf.set_random_seed} for behavior.
        dtype: The data type. Only floating point types are supported.

    Raises:
        ValueError: In case of an invalid value for the "scale", mode" or "distribution" arguments.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    VarianceScaling:
      scale: 0.5
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: VarianceScaling
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        VarianceScaling:
          scale: 1.
          mode: fan_out
    ```
    """
    IDENTIFIER = 'VarianceScaling'
    SCHEMA = VarianceScalingInitializerSchema

    def __init__(self, scale=1., mode='fan_in', distribution="normal", dtype='float32'):
        self.scale = scale
        self.mode = mode
        self.distribution = distribution
        self.dtype = dtype


class IdentityInitializerSchema(BaseSchema):
    gain = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return IdentityInitializerConfig


class IdentityInitializerConfig(BaseConfig):
    """Initializer that generates the identity matrix.

    Only use for 2D matrices.

    Args:
        gain: Multiplicative factor to apply to the identity matrix.
        dtype: The type of the output.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    Identity:
      gain: 0.5
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Identity
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        Identity:
          gain: 0.5
    ```
    """
    IDENTIFIER = 'Identity'
    SCHEMA = IdentityInitializerSchema

    def __init__(self, gain=1.):
        self.gain = gain


class OrthogonalInitializerSchema(BaseSchema):
    mean = fields.Number(allow_none=True)
    stddev = fields.Number(allow_none=True)
    gain = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return OrthogonalInitializerConfig


class OrthogonalInitializerConfig(BaseConfig):
    """Initializer that generates an orthogonal matrix.

    If the shape of the tensor to initialize is two-dimensional, it is initialized
    with an orthogonal matrix obtained from the QR decomposition of a matrix of
    uniform random numbers. If the matrix has fewer rows than columns then the
    output will have orthogonal rows. Otherwise, the output will have orthogonal
    columns.

    If the shape of the tensor to initialize is more than two-dimensional,
    a matrix of shape `(shape[0] * ... * shape[n - 2], shape[n - 1])`
    is initialized, where `n` is the length of the shape vector.
    The matrix is subsequently reshaped to give a tensor of the desired shape.

    Args:
        gain: multiplicative factor to apply to the orthogonal matrix
        dtype: The type of the output.
        seed: A Python integer. Used to create random seeds. See
            @{tf.set_random_seed} for behavior.

    Returns:
        An initializer.

    Polyaxonfile usage:

    ```yaml
    Orthogonal:
      gain: 0.5
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: Orthogonal
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer:
        Orthogonal:
          gain: 0.5
    ```
    """
    IDENTIFIER = 'Orthogonal'
    SCHEMA = OrthogonalInitializerSchema

    def __init__(self, gain=1., seed=None, dtype='float32'):
        self.seed = seed
        self.dtype = dtype
        self.gain = gain


class GlorotUniformInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return GlorotUniformInitializerConfig


class GlorotUniformInitializerConfig(BaseConfig):
    """Glorot uniform initializer, also called Xavier uniform initializer.

    It draws samples from a uniform distribution within [-limit, limit]
    where `limit` is `sqrt(6 / (fan_in + fan_out))`
    where `fan_in` is the number of input units in the weight tensor
    and `fan_out` is the number of output units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        Glorot & Bengio, AISTATS 2010
        http://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf

    Polyaxonfile usage:

    Using the default values

    ```yaml
    GlorotUniform:
    ```

    Using custom values

    ```yaml
    GlorotUniform:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: GlorotUniform
    ```
    """
    IDENTIFIER = 'GlorotUniform'
    SCHEMA = GlorotUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class GlorotNormalInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return GlorotNormalInitializerConfig


class GlorotNormalInitializerConfig(BaseConfig):
    """Glorot normal initializer, also called Xavier normal initializer.

    It draws samples from a truncated normal distribution centered on 0
    with `stddev = sqrt(2 / (fan_in + fan_out))`
    where `fan_in` is the number of input units in the weight tensor
    and `fan_out` is the number of output units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        Glorot & Bengio, AISTATS 2010
        http://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf

    Polyaxonfile usage:

    Using the default values

    ```yaml
    GlorotNormal:
    ```

    Using custom values

    ```yaml
    GlorotNormal:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: GlorotNormal
    ```
    """
    IDENTIFIER = 'GlorotNormal'
    SCHEMA = GlorotNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class HeUniformInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return HeUniformInitializerConfig


class HeUniformInitializerConfig(BaseConfig):
    """He uniform variance scaling initializer.

    It draws samples from a uniform distribution within [-limit, limit]
    where `limit` is `sqrt(6 / fan_in)`
    where `fan_in` is the number of input units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        He et al., http://arxiv.org/abs/1502.01852

    Polyaxonfile usage:

    Using the default values

    ```yaml
    HeUniform:
    ```

    Using custom values

    ```yaml
    HeUniform:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: HeUniform
    ```
    """
    IDENTIFIER = 'HeUniform'
    SCHEMA = HeUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class HeNormalInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return HeNormalInitializerConfig


class HeNormalInitializerConfig(BaseConfig):
    """He normal initializer.

    It draws samples from a truncated normal distribution centered on 0
    with `stddev = sqrt(2 / fan_in)`
    where `fan_in` is the number of input units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        He et al., http://arxiv.org/abs/1502.01852

    Polyaxonfile usage:

    Using the default values

    ```yaml
    HeNormal:
    ```

    Using custom values

    ```yaml
    HeNormal:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: HeNormal
    ```
    """
    IDENTIFIER = 'HeNormal'
    SCHEMA = HeNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class LecunUniformInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return LecunUniformInitializerConfig


class LecunUniformInitializerConfig(BaseConfig):
    """LeCun uniform initializer.

    It draws samples from a uniform distribution within [-limit, limit]
    where `limit` is `sqrt(3 / fan_in)`
    where `fan_in` is the number of input units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        LeCun 98, Efficient Backprop,
        http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf

    Polyaxonfile usage:

    Using the default values

    ```yaml
    LecunUniform:
    ```

    Using custom values

    ```yaml
    LecunUniform:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: LecunUniform
    ```
    """
    IDENTIFIER = 'LecunUniform'
    SCHEMA = LecunUniformInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class LecunNormalInitializerSchema(BaseSchema):
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return LecunNormalInitializerConfig


class LecunNormalInitializerConfig(BaseConfig):
    """LeCun normal initializer.

    It draws samples from a truncated normal distribution centered on 0
    with `stddev = sqrt(1 / fan_in)`
    where `fan_in` is the number of input units in the weight tensor.

    Args:
        seed: A Python integer. Used to seed the random generator.

    Returns:
        An initializer.

    References:
        - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)
        - [Efficient
        Backprop](http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf)

    Polyaxonfile usage:

    Using the default values

    ```yaml
    LecunNormal:
    ```

    Using custom values

    ```yaml
    LecunNormal:
      seed: 10
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_initializer: LecunNormal
    ```
    """
    IDENTIFIER = 'LecunNormal'
    SCHEMA = LecunNormalInitializerSchema

    def __init__(self, seed=None):
        self.seed = seed


class InitializerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'initializer'
    __configs__ = {
        ZerosInitializerConfig.IDENTIFIER: ZerosInitializerConfig,
        OnesInitializerConfig.IDENTIFIER: OnesInitializerConfig,
        ConstantInitializerConfig.IDENTIFIER: ConstantInitializerConfig,
        UniformInitializerConfig.IDENTIFIER: UniformInitializerConfig,
        NormalInitializerConfig.IDENTIFIER: NormalInitializerConfig,
        TruncatedNormalInitializerConfig.IDENTIFIER: TruncatedNormalInitializerConfig,
        VarianceScalingInitializerConfig.IDENTIFIER: VarianceScalingInitializerConfig,
        IdentityInitializerConfig.IDENTIFIER: IdentityInitializerConfig,
        OrthogonalInitializerConfig.IDENTIFIER: OrthogonalInitializerConfig,
        GlorotUniformInitializerConfig.IDENTIFIER: GlorotUniformInitializerConfig,
        GlorotNormalInitializerConfig.IDENTIFIER: GlorotNormalInitializerConfig,
        HeUniformInitializerConfig.IDENTIFIER: HeUniformInitializerConfig,
        HeNormalInitializerConfig.IDENTIFIER: HeNormalInitializerConfig,
        LecunUniformInitializerConfig.IDENTIFIER: LecunUniformInitializerConfig,
        LecunNormalInitializerConfig.IDENTIFIER: LecunNormalInitializerConfig,
    }
    __support_snake_case__ = True
