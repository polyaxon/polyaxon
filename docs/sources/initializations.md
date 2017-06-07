## zeros


```python
zeros(shape=None, dtype=<dtype: 'float32'>, name='zeros')
```


Zeros.

Initialize a tensor with all elements set to zero.

- __Args__:
	- __shape__: List of `int`. A shape to initialize a Tensor (optional).
	- __dtype__: The tensor data type.
	- __name__: name of the op.

- __Returns__:
	The Initializer, or an initialized `Tensor` if a shape is specified.


----

## uniform


```python
uniform(shape=None, minval=0, maxval=None, dtype=<dtype: 'float32'>, seed=None, name='Uniform')
```


Uniform.

Initialization with random values from a uniform distribution.

The generated values follow a uniform distribution in the range
`[minval, maxval)`. The lower bound `minval` is included in the range,
while the upper bound `maxval` is excluded.

For floats, the default range is `[0, 1)`.  For ints, at least `maxval`
must be specified explicitly.

In the integer case, the random integers are slightly biased unless
`maxval - minval` is an exact power of two.  The bias is small for values of
`maxval - minval` significantly smaller than the range of the output (either
`2**32` or `2**64`).

- __Args__:
	- __shape__: List of `int`. A shape to initialize a Tensor (optional).
	- __dtype__: The tensor data type. Only float are supported.
	- __seed__: `int`. Used to create a random seed for the distribution.
	- __name__: name of the op.

- __Returns__:
	The Initializer, or an initialized `Tensor` if shape is specified.



----

## uniform_scaling


```python
uniform_scaling(shape=None, factor=1.0, dtype=<dtype: 'float32'>, seed=None, name='UniformScaling')
```


Uniform Scaling.

Initialization with random values from uniform distribution without scaling
variance.

When initializing a deep network, it is in principle advantageous to keep
the scale of the input variance constant, so it does not explode or diminish
by reaching the final layer. If the input is `x` and the operation `x * W`,
and we want to initialize `W` uniformly at random, we need to pick `W` from

  [-sqrt(3) / sqrt(dim), sqrt(3) / sqrt(dim)]

to keep the scale intact, where `dim = W.shape[0]` (the size of the input).
A similar calculation for convolutional networks gives an analogous result
with `dim` equal to the product of the first 3 dimensions.  When
nonlinearities are present, we need to multiply this by a constant `factor`.
See [Sussillo et al., 2014](https://arxiv.org/abs/1412.6558)
([pdf](http://arxiv.org/pdf/1412.6558.pdf)) for deeper motivation, experiments
and the calculation of constants. In section 2.3 there, the constants were
numerically computed: for a linear layer it's 1.0, relu: ~1.43, tanh: ~1.15.

- __Args__:
	- __shape__: List of `int`. A shape to initialize a Tensor (optional).
	- __factor__: `float`. A multiplicative factor by which the values will be
	scaled.
	- __dtype__: The tensor data type. Only float are supported.
	- __seed__: `int`. Used to create a random seed for the distribution.
	- __name__: name of the op.

- __Returns__:
	The Initializer, or an initialized `Tensor` if shape is specified.



----

## normal


```python
normal(shape=None, mean=0.0, stddev=0.02, dtype=<dtype: 'float32'>, seed=None, name='Normal')
```


Normal.

Initialization with random values from a normal distribution.

- __Args__:
	- __shape__: List of `int`. A shape to initialize a Tensor (optional).
	- __mean__: Same as `dtype`. The mean of the truncated normal distribution.
	- __stddev__: Same as `dtype`. The standard deviation of the truncated
	normal distribution.
	- __dtype__: The tensor data type.
	- __seed__: `int`. Used to create a random seed for the distribution.
	- __scope__: scope to add the op to.
	- __name__: name of the op.

- __Returns__:
	The Initializer, or an initialized `Tensor` if shape is specified.



----

## truncated_normal


```python
truncated_normal(shape=None, mean=0.0, stddev=0.02, dtype=<dtype: 'float32'>, seed=None, name='TruncatedNormal')
```


Truncated Normal.

Initialization with random values from a normal truncated distribution.

The generated values follow a normal distribution with specified mean and
standard deviation, except that values whose magnitude is more than 2 standard
deviations from the mean are dropped and re-picked.

- __Args__:
	- __shape__: List of `int`. A shape to initialize a Tensor (optional).
	- __mean__: Same as `dtype`. The mean of the truncated normal distribution.
	- __stddev__: Same as `dtype`. The standard deviation of the truncated
	normal distribution.
	- __dtype__: The tensor data type.
	- __seed__: `int`. Used to create a random seed for the distribution.
	- __name__: name of the op.

- __Returns__:
	The Initializer, or an initialized `Tensor` if shape is specified.



----

## xavier


```python
xavier(uniform=True, seed=None, dtype=<dtype: 'float32'>, name='Xavier')
```


Xavier.

Returns an initializer performing "Xavier" initialization for weights.

This initializer is designed to keep the scale of the gradients roughly the
same in all layers. In uniform distribution this ends up being the range:
`x = sqrt(6. / (in + out)); [-x, x]` and for normal distribution a standard
deviation of `sqrt(3. / (in + out))` is used.

- __Args__:
	- __uniform__: Whether to use uniform or normal distributed random
	initialization.
	- __seed__: A Python integer. Used to create random seeds. See
	`set_random_seed` for behavior.
	- __dtype__: The data type. Only floating point types are supported.
	- __name__: name of the op.

- __Returns__:
	An initializer for a weight matrix.

- __References__:
	Understanding the difficulty of training deep feedforward neural
	networks. International conference on artificial intelligence and
	statistics. Xavier Glorot and Yoshua Bengio (2010).

- __Links__:
	- __[http__://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf]
	(http://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf)


----

## variance_scaling


```python
variance_scaling(factor=2.0, mode='FAN_IN', uniform=False, seed=None, dtype=<dtype: 'float32'>, name='Xavier')
```


Variance Scaling.

Returns an initializer that generates tensors without scaling variance.

When initializing a deep network, it is in principle advantageous to keep
the scale of the input variance constant, so it does not explode or diminish
by reaching the final layer. This initializer use the following formula:

```
if mode='FAN_IN': # Count only number of input connections.
  n = fan_in
elif mode='FAN_OUT': # Count only number of output connections.
  n = fan_out
elif mode='FAN_AVG': # Average number of inputs and output connections.
  n = (fan_in + fan_out)/2.0

  truncated_normal(shape, 0.0, stddev=sqrt(factor / n))
```

To get http://arxiv.org/pdf/1502.01852v1.pdf use (Default):
- factor=2.0 mode='FAN_IN' uniform=False

To get http://arxiv.org/abs/1408.5093 use:
- factor=1.0 mode='FAN_IN' uniform=True

To get http://jmlr.org/proceedings/papers/v9/glorot10a/glorot10a.pdf use:
- factor=1.0 mode='FAN_AVG' uniform=True.

To get xavier_initializer use either:
- factor=1.0 mode='FAN_AVG' uniform=True.
- factor=1.0 mode='FAN_AVG' uniform=False.

- __Args__:
	- __factor__: Float.  A multiplicative factor.
	- __mode__: String.  'FAN_IN', 'FAN_OUT', 'FAN_AVG'.
	- __uniform__: Whether to use uniform or normal distributed random
	initialization.
	- __seed__: A Python integer. Used to create random seeds. See
	`set_random_seed` for behavior.
	- __dtype__: The data type. Only floating point types are supported.
	- __name__: name of the op.

- __Returns__:
	An initializer that generates tensors with unit variance.

- __Raises__:
	- __ValueError__: if `dtype` is not a floating point type.
	- __TypeError__: if `mode` is not in ['FAN_IN', 'FAN_OUT', 'FAN_AVG'].
