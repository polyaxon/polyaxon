<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L32)</span>
## MaskingConfig

```python
polyaxon_schemas.layers.core.MaskingConfig(mask_value=0.0)
```

Masks a sequence by using a mask value to skip timesteps.

For each timestep in the input tensor (dimension #1 in the tensor),
if all values in the input tensor at that timestep
are equal to `mask_value`, then the timestep will be masked (skipped)
in all downstream layers (as long as they support masking).

If any downstream layer does not support masking yet receives such
an input mask, an exception will be raised.

- __Example__:


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L90)</span>
## DropoutConfig

```python
polyaxon_schemas.layers.core.DropoutConfig(rate, noise_shape=None, seed=None)
```

Applies Dropout to the input.

Dropout consists in randomly setting
a fraction `rate` of input units to 0 at each update during training time,
which helps prevent overfitting.

- __Args__:

	- __rate__: float between 0 and 1. Fraction of the input units to drop.

	- __noise_shape__: 1D integer tensor representing the shape of the

		binary dropout mask that will be multiplied with the input.
		For instance, if your inputs have shape
		`(batch_size, timesteps, features)` and
		you want the dropout mask to be the same for all timesteps,
		you can use `noise_shape=(batch_size, 1, features)`.
	- __seed__: A Python integer to use as random seed.


Polyaxonfile usage:

```yaml
Dropout:
  rate: 0.5
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L137)</span>
## SpatialDropout1DConfig

```python
polyaxon_schemas.layers.core.SpatialDropout1DConfig(rate, noise_shape=None, seed=None)
```

Spatial 1D version of Dropout.

This version performs the same function as Dropout, however it drops
entire 1D feature maps instead of individual elements. If adjacent frames
within feature maps are strongly correlated (as is normally the case in
early convolution layers) then regular dropout will not regularize the
activations and will otherwise just result in an effective learning rate
decrease. In this case, SpatialDropout1D will help promote independence
between feature maps and should be used instead.

- __Args__:

	- __rate__: float between 0 and 1. Fraction of the input units to drop.


Input shape:
	3D tensor with shape:
	`(samples, timesteps, channels)`

Output shape:
	Same as input

- __References__:

	- [Efficient Object Localization Using Convolutional
	  Networks](https://arxiv.org/abs/1411.4280)

Polyaxonfile usage:

```yaml
SpatialDropout1D:
  rate: 0.5
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L189)</span>
## SpatialDropout2DConfig

```python
polyaxon_schemas.layers.core.SpatialDropout2DConfig(rate, data_format=None)
```

Spatial 2D version of Dropout.

This version performs the same function as Dropout, however it drops
entire 2D feature maps instead of individual elements. If adjacent pixels
within feature maps are strongly correlated (as is normally the case in
early convolution layers) then regular dropout will not regularize the
activations and will otherwise just result in an effective learning rate
decrease. In this case, SpatialDropout2D will help promote independence
between feature maps and should be used instead.

- __Args__:

	- __rate__: float between 0 and 1. Fraction of the input units to drop.

	- __data_format__: 'channels_first' or 'channels_last'.

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

- __References__:

	- [Efficient Object Localization Using Convolutional
	  Networks](https://arxiv.org/abs/1411.4280)

Polyaxonfile usage:

```yaml
SpatialDropout2D:
  rate: 0.5
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L252)</span>
## SpatialDropout3DConfig

```python
polyaxon_schemas.layers.core.SpatialDropout3DConfig(rate, data_format=None)
```

Spatial 3D version of Dropout.

This version performs the same function as Dropout, however it drops
entire 3D feature maps instead of individual elements. If adjacent voxels
within feature maps are strongly correlated (as is normally the case in
early convolution layers) then regular dropout will not regularize the
activations and will otherwise just result in an effective learning rate
decrease. In this case, SpatialDropout3D will help promote independence
between feature maps and should be used instead.

- __Args__:

	- __rate__: float between 0 and 1. Fraction of the input units to drop.

	- __data_format__: 'channels_first' or 'channels_last'.

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

- __References__:

	- [Efficient Object Localization Using Convolutional
	  Networks](https://arxiv.org/abs/1411.4280)

Polyaxonfile usage:

```yaml
SpatialDropout3D:
  rate: 0.5
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L313)</span>
## ActivationConfig

```python
polyaxon_schemas.layers.core.ActivationConfig(activation)
```

Applies an activation function to an output.

- __Args__:

	- __activation__: name of activation function.


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L357)</span>
## ReshapeConfig

```python
polyaxon_schemas.layers.core.ReshapeConfig(target_shape)
```

Reshapes an output to a certain shape.

- __Args__:

	- __target_shape__: target shape. Tuple of integers,

		does not include the samples dimension (batch size).

Input shape:
	Arbitrary, although all dimensions in the input shaped must be fixed.
	Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	`(batch_size,) + target_shape`

- __Example__:


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L416)</span>
## PermuteConfig

```python
polyaxon_schemas.layers.core.PermuteConfig(dims)
```

Permutes the dimensions of the input according to a given pattern.

Useful for e.g. connecting RNNs and convnets together.

- __Args__:

	- __dims__: Tuple of integers. Permutation pattern, does not include the

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

- __Example__:


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L472)</span>
## FlattenConfig

```python
polyaxon_schemas.layers.core.FlattenConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Flattens the input. Does not affect the batch size.

- __Example__:


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L512)</span>
## RepeatVectorConfig

```python
polyaxon_schemas.layers.core.RepeatVectorConfig(n)
```

Repeats the input n times.

- __Example__:


```python
x = Dense(32)(x)
# now: x.output_shape == (None, 32)
# note: `None` is the batch dimension

x = RepeatVector(3)(x)
# now: x.output_shape == (None, 3, 32)
```

- __Args__:

	- __n__: integer, repetition factor.


Input shape:
	2D tensor of shape `(num_samples, features)`.

Output shape:
	3D tensor of shape `(num_samples, n, features)`.
	
Polyaxonfile usage:

```yaml
RepeatVector:
  n: 32
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L577)</span>
## DenseConfig

```python
polyaxon_schemas.layers.core.DenseConfig(units, activation=None, use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x103fdd390>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x103fdd358>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Just your regular densely-connected NN layer.

`Dense` implements the operation:
`output = activation(dot(input, kernel) + bias)`
where `activation` is the element-wise activation function
passed as the `activation` argument, `kernel` is a weights matrix
created by the layer, and `bias` is a bias vector created by the layer
(only applicable if `use_bias` is `True`).

- __Note__: if the input to the layer has a rank greater than 2, then

it is flattened prior to the initial dot product with `kernel`.

- __Example__:


```python
# as first layer in a sequential model:
x = Dense(32)(x)
# now the model will take as input arrays of shape (*, 16)
# and output arrays of shape (*, 32)
```

- __Args__:

	- __units__: Positive integer, dimensionality of the output space.

	- __activation__: Activation function to use.

		If you don't specify anything, no activation is applied
		(ie. "linear" activation: `a(x) = x`).
	- __use_bias__: Boolean, whether the layer uses a bias vector.

	- __kernel_initializer__: Initializer for the `kernel` weights matrix.

	- __bias_initializer__: Initializer for the bias vector.

	- __kernel_regularizer__: Regularizer function applied to

		the `kernel` weights matrix.
	- __bias_regularizer__: Regularizer function applied to the bias vector.

	- __activity_regularizer__: Regularizer function applied to

		the output of the layer (its "activation")..
	- __kernel_constraint__: Constraint function applied to

		the `kernel` weights matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L678)</span>
## ActivityRegularizationConfig

```python
polyaxon_schemas.layers.core.ActivityRegularizationConfig(l1=0.0, l2=0.0)
```

Layer that applies an update to the cost function based input activity.

- __Args__:

	- __l1__: L1 regularization factor (positive float).

	- __l2__: L2 regularization factor (positive float).


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/core.py#L725)</span>
## CastConfig

```python
polyaxon_schemas.layers.core.CastConfig(dtype)
```

Casts a tensor to a new type.

The operation casts `x` (in case of `Tensor`) or `x.values`
(in case of `SparseTensor`) to `dtype`.

For example:

```python
x = tf.constant([1.8, 2.2], dtype=tf.float32)
x = Cast(dtype=tf.int32)(x)  # [1, 2], dtype=tf.int32
```

- __Args__:

  - __x__: A `Tensor` or `SparseTensor`.

  - __dtype__: The destination type.

  - __name__: A name for the operation (optional).


- __Returns__:

  A `Tensor` or `SparseTensor` with same shape as `x`.

- __Raises__:

  - __TypeError__: If `x` cannot be cast to the `dtype`.


Polyaxonfile usage:

```yaml
Cast:
  dtype: float32
```
