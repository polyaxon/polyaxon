<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L31)</span>
## Masking

```python
tensorflow.contrib.keras.python.keras.layers.core.Masking(mask_value=0.0)
```

Masks a sequence by using a mask value to skip timesteps.

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
  model = Sequential()
  model.add(Masking(mask_value=0., input_shape=(timesteps, features)))
  model.add(LSTM(32))
  ```
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L36)</span>
## Dropout

```python
tensorflow.contrib.keras.python.keras.layers.core.Dropout(rate, noise_shape=None, seed=None)
```

Applies Dropout to the input.

  Dropout consists in randomly setting
  a fraction `rate` of input units to 0 at each update during training time,
  which helps prevent overfitting.

  Arguments:
  - __rate__: float between 0 and 1. Fraction of the input units to drop.
  - __noise_shape__: 1D integer tensor representing the shape of the
	  binary dropout mask that will be multiplied with the input.
	  For instance, if your inputs have shape
	  `(batch_size, timesteps, features)` and
	  you want the dropout mask to be the same for all timesteps,
	  you can use `noise_shape=(batch_size, 1, features)`.
  - __seed__: A Python integer to use as random seed.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L41)</span>
## SpatialDropout1D

```python
tensorflow.contrib.keras.python.keras.layers.core.SpatialDropout1D(rate)
```

Spatial 1D version of Dropout.

  This version performs the same function as Dropout, however it drops
  entire 1D feature maps instead of individual elements. If adjacent frames
  within feature maps are strongly correlated (as is normally the case in
  early convolution layers) then regular dropout will not regularize the
  activations and will otherwise just result in an effective learning rate
  decrease. In this case, SpatialDropout1D will help promote independence
  between feature maps and should be used instead.

  Arguments:
  - __rate__: float between 0 and 1. Fraction of the input units to drop.

  Input shape:
  3D tensor with shape:
  `(samples, timesteps, channels)`

  Output shape:
  Same as input

  References:
  - [Efficient Object Localization Using Convolutional
	Networks](https://arxiv.org/abs/1411.4280)
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L46)</span>
## SpatialDropout2D

```python
tensorflow.contrib.keras.python.keras.layers.core.SpatialDropout2D(rate, data_format=None)
```

Spatial 2D version of Dropout.

  This version performs the same function as Dropout, however it drops
  entire 2D feature maps instead of individual elements. If adjacent pixels
  within feature maps are strongly correlated (as is normally the case in
  early convolution layers) then regular dropout will not regularize the
  activations and will otherwise just result in an effective learning rate
  decrease. In this case, SpatialDropout2D will help promote independence
  between feature maps and should be used instead.

  Arguments:
  - __rate__: float between 0 and 1. Fraction of the input units to drop.
  - __data_format__: 'channels_first' or 'channels_last'.
	  In 'channels_first' mode, the channels dimension
	  (the depth) is at index 1,
	  in 'channels_last' mode is it at index 3.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L51)</span>
## SpatialDropout3D

```python
tensorflow.contrib.keras.python.keras.layers.core.SpatialDropout3D(rate, data_format=None)
```

Spatial 3D version of Dropout.

  This version performs the same function as Dropout, however it drops
  entire 3D feature maps instead of individual elements. If adjacent voxels
  within feature maps are strongly correlated (as is normally the case in
  early convolution layers) then regular dropout will not regularize the
  activations and will otherwise just result in an effective learning rate
  decrease. In this case, SpatialDropout3D will help promote independence
  between feature maps and should be used instead.

  Arguments:
  - __rate__: float between 0 and 1. Fraction of the input units to drop.
  - __data_format__: 'channels_first' or 'channels_last'.
	  In 'channels_first' mode, the channels dimension (the depth)
	  is at index 1, in 'channels_last' mode is it at index 4.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L56)</span>
## Activation

```python
tensorflow.contrib.keras.python.keras.layers.core.Activation(activation)
```

Applies an activation function to an output.

  Arguments:
  - __activation__: name of activation function to use
	  or alternatively, a Theano or TensorFlow operation.

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as input.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L61)</span>
## Reshape

```python
tensorflow.contrib.keras.python.keras.layers.core.Reshape(target_shape)
```

Reshapes an output to a certain shape.

  Arguments:
  - __target_shape__: target shape. Tuple of integers,
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
  model = Sequential()
  model.add(Reshape((3, 4), input_shape=(12,)))
  # now: model.output_shape == (None, 3, 4)
  # note: `None` is the batch dimension

  # as intermediate layer in a Sequential model
  model.add(Reshape((6, 2)))
  # now: model.output_shape == (None, 6, 2)

  # also supports shape inference using `-1` as dimension
  model.add(Reshape((-1, 2, 2)))
  # now: model.output_shape == (None, 3, 2, 2)
  ```
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L66)</span>
## Permute

```python
tensorflow.contrib.keras.python.keras.layers.core.Permute(dims)
```

Permutes the dimensions of the input according to a given pattern.

  Useful for e.g. connecting RNNs and convnets together.

  Example:

  ```python
  model = Sequential()
  model.add(Permute((2, 1), input_shape=(10, 64)))
  # now: model.output_shape == (None, 64, 10)
  # note: `None` is the batch dimension
  ```

  Arguments:
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L71)</span>
## Flatten

```python
tensorflow.contrib.keras.python.keras.layers.core.Flatten()
```

Flattens the input. Does not affect the batch size.

  Example:

  ```python
  model = Sequential()
  model.add(Convolution2D(64, 3, 3,
				  border_mode='same',
				  input_shape=(3, 32, 32)))
  # now: model.output_shape == (None, 64, 32, 32)

  model.add(Flatten())
  # now: model.output_shape == (None, 65536)
  ```
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L76)</span>
## RepeatVector

```python
tensorflow.contrib.keras.python.keras.layers.core.RepeatVector(n)
```

Repeats the input n times.

  Example:

  ```python
  model = Sequential()
  model.add(Dense(32, input_dim=32))
  # now: model.output_shape == (None, 32)
  # note: `None` is the batch dimension

  model.add(RepeatVector(3))
  # now: model.output_shape == (None, 3, 32)
  ```

  Arguments:
  - __n__: integer, repetition factor.

  Input shape:
  2D tensor of shape `(num_samples, features)`.

  Output shape:
  3D tensor of shape `(num_samples, n, features)`.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L150)</span>
## Lambda

```python
tensorflow.contrib.keras.python.keras.layers.core.Lambda(function, mask=None, arguments=None)
```

Wraps arbitrary expression as a `Layer` object.

  Examples:

  ```python
  # add a x -> x^2 layer
  model.add(Lambda(lambda x: x ** 2))
  ```
  ```python
  # add a layer that returns the concatenation
  # of the positive part of the input and
  # the opposite of the negative part

  def antirectifier(x):
	  x -= K.mean(x, axis=1, keepdims=True)
	  x = K.l2_normalize(x, axis=1)
	  pos = K.relu(x)
	  neg = K.relu(-x)
	  return K.concatenate([pos, neg], axis=1)

  model.add(Lambda(antirectifier))
  ```

  Arguments:
  - __function__: The function to be evaluated.
	  Takes input tensor as first argument.
  - __arguments__: optional dictionary of keyword arguments to be passed
	  to the function.

  Input shape:
  Arbitrary. Use the keyword argument input_shape
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Specified by `output_shape` argument
  (or auto-inferred when using TensorFlow).
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L81)</span>
## Dense

```python
polyaxon.layers.core.Dense(units, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Just your regular densely-connected NN layer.

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
  model = Sequential()
  model.add(Dense(32, input_shape=(16,)))
  # now the model will take as input arrays of shape (*, 16)
  # and output arrays of shape (*, 32)

  # after the first layer, you don't need to specify
  # the size of the input anymore:
  model.add(Dense(32))
  ```

  Arguments:
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L111)</span>
## ActivityRegularization

```python
tensorflow.contrib.keras.python.keras.layers.core.ActivityRegularization(l1=0.0, l2=0.0)
```

Layer that applies an update to the cost function based input activity.

  Arguments:
  - __l1__: L1 regularization factor (positive float).
  - __l2__: L2 regularization factor (positive float).

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as input.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L116)</span>
## Cast

```python
polyaxon.layers.core.Cast(dtype='float32')
```

Casts a tensor to a new type.

The operation casts `x` (in case of `Tensor`) or `x.values`
(in case of `SparseTensor`) to `dtype`.

For example:

```python
# tensor `a` is [1.8, 2.2], dtype=tf.float
>>> tf.cast(a, tf.int32) ==> [1, 2]  # dtype=tf.int32
```

- __Args__:
	- __x__: A `Tensor` or `SparseTensor`.
	- __dtype__: The destination type.
	- __name__: A name for the operation (optional).

- __Returns__:
	A `Tensor` or `SparseTensor` with same shape as `x`.

- __Raises__:
	- __TypeError__: If `x` cannot be cast to the `dtype`.
