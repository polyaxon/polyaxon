<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L25)</span>
## ZerosInitializerConfig

```python
polyaxon_schemas.initializations.ZerosInitializerConfig(dtype='float32')
```

Initializer that generates tensors initialized to 0.

- __Args__:

	- __dtype__: The data type.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L80)</span>
## OnesInitializerConfig

```python
polyaxon_schemas.initializations.OnesInitializerConfig(dtype='float32')
```

Initializer that generates tensors initialized to 1.

- __Args__:

	- __dtype__: The data type.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L136)</span>
## ConstantInitializerConfig

```python
polyaxon_schemas.initializations.ConstantInitializerConfig(value=0, dtype='float32')
```

Initializer that generates tensors with constant values.

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

- __Args__:

	- __value__: A Python scalar, list of values, or a N-dimensional numpy array. All

		elements of the initialized variable will be set to the corresponding
		value in the `value` argument.
	- __dtype__: The data type.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L206)</span>
## UniformInitializerConfig

```python
polyaxon_schemas.initializations.UniformInitializerConfig(minval=0, maxval=None, seed=None, dtype='float32')
```

Initializer that generates tensors with a uniform distribution.

- __Args__:

	- __minval__: A python scalar or a scalar tensor. Lower bound of the range

		of random values to generate.
	- __maxval__: A python scalar or a scalar tensor. Upper bound of the range

		of random values to generate.  Defaults to 1 for float types.
	- __seed__: A Python integer. Used to create random seeds. See

		@{tf.set_random_seed} for behavior.
	- __dtype__: The data type.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L277)</span>
## NormalInitializerConfig

```python
polyaxon_schemas.initializations.NormalInitializerConfig(mean=0.0, stddev=1.0, seed=None, dtype='float32')
```

Initializer that generates tensors with a normal distribution.

- __Args__:

	- __mean__: a python scalar or a scalar tensor. Mean of the random values to generate.

	- __stddev__: a python scalar or a scalar tensor. Standard deviation of the

		random values to generate.
	- __seed__: A Python integer. Used to create random seeds. See

		@{tf.set_random_seed} for behavior.
	- __dtype__: The data type. Only floating point types are supported.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L345)</span>
## TruncatedNormalInitializerConfig

```python
polyaxon_schemas.initializations.TruncatedNormalInitializerConfig(mean=0.0, stddev=1.0, seed=None, dtype='float32')
```

Initializer that generates a truncated normal distribution.

These values are similar to values from a `random_normal_initializer`
except that values more than two standard deviations from the mean
are discarded and re-drawn. This is the recommended initializer for
neural network weights and filters.

- __Args__:

	- __mean__: a python scalar or a scalar tensor. Mean of the random values to generate.

	- __stddev__: a python scalar or a scalar tensor. Standard deviation of the

		random values to generate.
	- __seed__: A Python integer. Used to create random seeds. See

		@{tf.set_random_seed} for behavior.
	- __dtype__: The data type. Only floating point types are supported.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L420)</span>
## VarianceScalingInitializerConfig

```python
polyaxon_schemas.initializations.VarianceScalingInitializerConfig(scale=1.0, mode='fan_in', distribution='normal', dtype='float32')
```

Initializer capable of adapting its scale to the shape of weights tensors.

With `distribution="normal"`, samples are drawn from a truncated normal
distribution centered on zero, with `stddev = sqrt(scale / n)`
where n is:
  - number of input units in the weight tensor, if mode = "fan_in"
  - number of output units, if mode = "fan_out"
  - average of the numbers of input and output units, if mode = "fan_avg"

With `distribution="uniform"`, samples are drawn from a uniform distribution
within [-limit, limit], with `limit = sqrt(3 * scale / n)`.

- __Args__:

	- __scale__: Scaling factor (positive float).

	- __mode__: One of "fan_in", "fan_out", "fan_avg".

	- __distribution__: Random distribution to use. One of "normal", "uniform".

	- __seed__: A Python integer. Used to create random seeds. See

		@{tf.set_random_seed} for behavior.
	- __dtype__: The data type. Only floating point types are supported.


- __Raises__:

	- __ValueError__: In case of an invalid value for the "scale", mode" or "distribution" arguments.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L500)</span>
## IdentityInitializerConfig

```python
polyaxon_schemas.initializations.IdentityInitializerConfig(gain=1.0)
```

Initializer that generates the identity matrix.

Only use for 2D matrices.

- __Args__:

	- __gain__: Multiplicative factor to apply to the identity matrix.

	- __dtype__: The type of the output.


- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L563)</span>
## OrthogonalInitializerConfig

```python
polyaxon_schemas.initializations.OrthogonalInitializerConfig(gain=1.0, seed=None, dtype='float32')
```

Initializer that generates an orthogonal matrix.

If the shape of the tensor to initialize is two-dimensional, it is initialized
with an orthogonal matrix obtained from the QR decomposition of a matrix of
uniform random numbers. If the matrix has fewer rows than columns then the
output will have orthogonal rows. Otherwise, the output will have orthogonal
columns.

If the shape of the tensor to initialize is more than two-dimensional,
a matrix of shape `(shape[0] * ... * shape[n - 2], shape[n - 1])`
is initialized, where `n` is the length of the shape vector.
The matrix is subsequently reshaped to give a tensor of the desired shape.

- __Args__:

	- __gain__: multiplicative factor to apply to the orthogonal matrix

	- __dtype__: The type of the output.

	- __seed__: A Python integer. Used to create random seeds. See

		@{tf.set_random_seed} for behavior.

- __Returns__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L637)</span>
## GlorotUniformInitializerConfig

```python
polyaxon_schemas.initializations.GlorotUniformInitializerConfig(seed=None)
```

Glorot uniform initializer, also called Xavier uniform initializer.

It draws samples from a uniform distribution within [-limit, limit]
where `limit` is `sqrt(6 / (fan_in + fan_out))`
where `fan_in` is the number of input units in the weight tensor
and `fan_out` is the number of output units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

	Glorot & Bengio, AISTATS 2010
	- __http__://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L701)</span>
## GlorotNormalInitializerConfig

```python
polyaxon_schemas.initializations.GlorotNormalInitializerConfig(seed=None)
```

Glorot normal initializer, also called Xavier normal initializer.

It draws samples from a truncated normal distribution centered on 0
with `stddev = sqrt(2 / (fan_in + fan_out))`
where `fan_in` is the number of input units in the weight tensor
and `fan_out` is the number of output units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

	Glorot & Bengio, AISTATS 2010
	- __http__://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L765)</span>
## HeUniformInitializerConfig

```python
polyaxon_schemas.initializations.HeUniformInitializerConfig(seed=None)
```

He uniform variance scaling initializer.

It draws samples from a uniform distribution within [-limit, limit]
where `limit` is `sqrt(6 / fan_in)`
where `fan_in` is the number of input units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L827)</span>
## HeNormalInitializerConfig

```python
polyaxon_schemas.initializations.HeNormalInitializerConfig(seed=None)
```

He normal initializer.

It draws samples from a truncated normal distribution centered on 0
with `stddev = sqrt(2 / fan_in)`
where `fan_in` is the number of input units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L889)</span>
## LecunUniformInitializerConfig

```python
polyaxon_schemas.initializations.LecunUniformInitializerConfig(seed=None)
```

LeCun uniform initializer.

It draws samples from a uniform distribution within [-limit, limit]
where `limit` is `sqrt(3 / fan_in)`
where `fan_in` is the number of input units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

	LeCun 98, Efficient Backprop,
	- __http__://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/initializations.py#L952)</span>
## LecunNormalInitializerConfig

```python
polyaxon_schemas.initializations.LecunNormalInitializerConfig(seed=None)
```

LeCun normal initializer.

It draws samples from a truncated normal distribution centered on 0
with `stddev = sqrt(1 / fan_in)`
where `fan_in` is the number of input units in the weight tensor.

- __Args__:

	- __seed__: A Python integer. Used to seed the random generator.


- __Returns__:

	An initializer.

- __References__:

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
