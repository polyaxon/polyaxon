<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L12)</span>
## Zeros

```python
polyaxon.initializations.Zeros(dtype=<dtype: 'float32'>)
```

Initializer that generates tensors initialized to 0.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L17)</span>
## Ones

```python
polyaxon.initializations.Ones(dtype=<dtype: 'float32'>)
```

Initializer that generates tensors initialized to 1.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L22)</span>
## Constant

```python
polyaxon.initializations.Constant(value=0, dtype=<dtype: 'float32'>, verify_shape=False)
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
  - __verify_shape__: Boolean that enables verification of the shape of `value`. If
  `True`, the initializer will throw an error if the shape of `value` is not
  compatible with the shape of the initialized tensor.

- __Examples__:
The following example can be rewritten using a numpy.ndarray instead
of the `value` list, even reshaped, as shown in the two commented lines
below the `value` list initialization.

  ```python
>>> import numpy as np
>>> import tensorflow as tf

>>> value = [0, 1, 2, 3, 4, 5, 6, 7]
>>> # value = np.array(value)
>>> # value = value.reshape([2, 4])
>>> init = tf.constant_initializer(value)

>>> print('fitting shape:')
>>> with tf.Session():
>>>   x = tf.get_variable('x', shape=[2, 4], initializer=init)
>>>   x.initializer.run()
>>>   print(x.eval())

fitting shape:
[[ 0.  1.  2.  3.]
 [ 4.  5.  6.  7.]]

>>> print('larger shape:')
>>> with tf.Session():
>>>   x = tf.get_variable('x', shape=[3, 4], initializer=init)
>>>   x.initializer.run()
>>>   print(x.eval())

larger shape:
[[ 0.  1.  2.  3.]
 [ 4.  5.  6.  7.]
 [ 7.  7.  7.  7.]]

>>> print('smaller shape:')
>>> with tf.Session():
>>>   x = tf.get_variable('x', shape=[2, 3], initializer=init)

  - __ValueError__: Too many elements provided. Needed at most 6, but received 8

>>> print('shape verification:')
>>> init_verify = tf.constant_initializer(value, verify_shape=True)
>>> with tf.Session():
>>>   x = tf.get_variable('x', shape=[3, 4], initializer=init_verify)

  - __TypeError__: Expected Tensor's shape: (3, 4), got (8,).
  ```
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L27)</span>
## Uniform

```python
polyaxon.initializations.Uniform(minval=0, maxval=None, seed=None, dtype=<dtype: 'float32'>)
```

Initializer that generates tensors with a uniform distribution.

- __Args__:
  - __minval__: A python scalar or a scalar tensor. Lower bound of the range
  of random values to generate.
  - __maxval__: A python scalar or a scalar tensor. Upper bound of the range
  of random values to generate.  Defaults to 1 for float types.
  - __seed__: A Python integer. Used to create random seeds. See
  @{tf.set_random_seed}
  for behavior.
  - __dtype__: The data type.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L32)</span>
## Normal

```python
polyaxon.initializations.Normal(mean=0.0, stddev=1.0, seed=None, dtype=<dtype: 'float32'>)
```

Initializer that generates tensors with a normal distribution.

- __Args__:
  - __mean__: a python scalar or a scalar tensor. Mean of the random values
  to generate.
  - __stddev__: a python scalar or a scalar tensor. Standard deviation of the
  random values to generate.
  - __seed__: A Python integer. Used to create random seeds. See
  @{tf.set_random_seed}
  for behavior.
  - __dtype__: The data type. Only floating point types are supported.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L37)</span>
## TruncatedNormal

```python
polyaxon.initializations.TruncatedNormal(mean=0.0, stddev=1.0, seed=None, dtype=<dtype: 'float32'>)
```

Initializer that generates a truncated normal distribution.

  These values are similar to values from a `random_normal_initializer`
  except that values more than two standard deviations from the mean
  are discarded and re-drawn. This is the recommended initializer for
  neural network weights and filters.

- __Args__:
  - __mean__: a python scalar or a scalar tensor. Mean of the random values
  to generate.
  - __stddev__: a python scalar or a scalar tensor. Standard deviation of the
  random values to generate.
  - __seed__: A Python integer. Used to create random seeds. See
  @{tf.set_random_seed}
  for behavior.
  - __dtype__: The data type. Only floating point types are supported.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L42)</span>
## VarianceScaling

```python
polyaxon.initializations.VarianceScaling(scale=1.0, mode='fan_in', distribution='normal', seed=None, dtype=<dtype: 'float32'>)
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

- __Arguments__:
  - __scale__: Scaling factor (positive float).
  - __mode__: One of "fan_in", "fan_out", "fan_avg".
  - __distribution__: Random distribution to use. One of "normal", "uniform".
  - __seed__: A Python integer. Used to create random seeds. See
  @{tf.set_random_seed}
  for behavior.
  - __dtype__: The data type. Only floating point types are supported.

- __Raises__:
  - __ValueError__: In case of an invalid value for the "scale", mode" or
  "distribution" arguments.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L47)</span>
## Orthogonal

```python
polyaxon.initializations.Orthogonal(gain=1.0, seed=None, dtype=<dtype: 'float32'>)
```

Initializer that generates an orthogonal matrix.

  If the shape of the tensor to initialize is two-dimensional, i is initialized
  with an orthogonal matrix obtained from the singular value decomposition of a
  matrix of uniform random numbers.

  If the shape of the tensor to initialize is more than two-dimensional,
  a matrix of shape `(shape[0] * ... * shape[n - 2], shape[n - 1])`
  is initialized, where `n` is the length of the shape vector.
  The matrix is subsequently reshaped to give a tensor of the desired shape.

- __Args__:
  - __gain__: multiplicative factor to apply to the orthogonal matrix
  - __dtype__: The type of the output.
  - __seed__: A Python integer. Used to create random seeds. See
  @{tf.set_random_seed}
  for behavior.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L52)</span>
## Identity

```python
polyaxon.initializations.Identity(gain=1.0)
```

Initializer that generates the identity matrix.

  Only use for square 2D matrices.

- __Arguments__:
	- __gain__: Multiplicative factor to apply to the identity matrix.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L57)</span>
## GlorotUniform

```python
polyaxon.initializations.GlorotUniform(seed=None)
```

Glorot uniform initializer, also called Xavier uniform initializer.

  It draws samples from a uniform distribution within [-limit, limit]
  where `limit` is `sqrt(6 / (fan_in + fan_out))`
  where `fan_in` is the number of input units in the weight tensor
  and `fan_out` is the number of output units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  Glorot & Bengio, AISTATS 2010
	- __http__://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L68)</span>
## GlorotNormal

```python
polyaxon.initializations.GlorotNormal(seed=None)
```

Glorot normal initializer, also called Xavier normal initializer.

  It draws samples from a truncated normal distribution centered on 0
  with `stddev = sqrt(2 / (fan_in + fan_out))`
  where `fan_in` is the number of input units in the weight tensor
  and `fan_out` is the number of output units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  Glorot & Bengio, AISTATS 2010
	- __http__://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L79)</span>
## HeUniform

```python
polyaxon.initializations.HeUniform(seed=None)
```

He uniform variance scaling initializer.

  It draws samples from a uniform distribution within [-limit, limit]
  where `limit` is `sqrt(6 / fan_in)`
  where `fan_in` is the number of input units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  He et al., http://arxiv.org/abs/1502.01852
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L90)</span>
## HeNormal

```python
polyaxon.initializations.HeNormal(seed=None)
```

He normal initializer.

  It draws samples from a truncated normal distribution centered on 0
  with `stddev = sqrt(2 / fan_in)`
  where `fan_in` is the number of input units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  He et al., http://arxiv.org/abs/1502.01852
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L101)</span>
## LecunUniform

```python
polyaxon.initializations.LecunUniform(seed=None)
```

LeCun uniform initializer.

  It draws samples from a uniform distribution within [-limit, limit]
  where `limit` is `sqrt(3 / fan_in)`
  where `fan_in` is the number of input units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  LeCun 98, Efficient Backprop,
	- __http__://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/initializations.py#L112)</span>
## LecunNormal

```python
polyaxon.initializations.LecunNormal(seed=None)
```

LeCun normal initializer.

  It draws samples from a truncated normal distribution centered on 0
  with `stddev = sqrt(1 / fan_in)`
  where `fan_in` is the number of input units in the weight tensor.

- __Arguments__:
	- __seed__: A Python integer. Used to seed the random generator.

- __Returns__:
  An initializer.

- __References__:
  - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)
  - [Efficient
  Backprop](http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf)
  