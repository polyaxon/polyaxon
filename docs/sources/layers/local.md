<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/local.py#L13)</span>
## LocallyConnected1D

```python
polyaxon.layers.local.LocallyConnected1D(filters, kernel_size, strides=1, padding='valid', data_format=None, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Locally-connected layer for 1D inputs.

  The `LocallyConnected1D` layer works similarly to
  the `Conv1D` layer, except that weights are unshared,
  that is, a different set of filters is applied at each different patch
  of the input.

- __Example__:
  ```python
  # apply a unshared weight convolution 1d of length 3 to a sequence with
  # 10 timesteps, with 64 output filters
  model = Sequential()
  model.add(LocallyConnected1D(64, 3, input_shape=(10, 32)))
  # now model.output_shape == (None, 8, 64)
  # add a new conv1d on top
  model.add(LocallyConnected1D(32, 3))
  # now model.output_shape == (None, 6, 32)
  ```

- __Arguments__:
	- __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
	- __kernel_size__: An integer or tuple/list of a single integer,
	  specifying the length of the 1D convolution window.
	- __strides__: An integer or tuple/list of a single integer,
	  specifying the stride length of the convolution.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
	- __padding__: Currently only supports `"valid"` (case-insensitive).
	  `"same"` may be supported in the future.
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
	- __kernel_constraint__: Constraint function applied to the kernel matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.

  Input shape:
  3D tensor with shape: `(batch_size, steps, input_dim)`

  Output shape:
  3D tensor with shape: `(batch_size, new_steps, filters)`
  `steps` value might have changed due to padding or strides.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/local.py#L18)</span>
## LocallyConnected2D

```python
polyaxon.layers.local.LocallyConnected2D(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Locally-connected layer for 2D inputs.

  The `LocallyConnected2D` layer works similarly
  to the `Conv2D` layer, except that weights are unshared,
  that is, a different set of filters is applied at each
  different patch of the input.

- __Examples__:
  ```python
  # apply a 3x3 unshared weights convolution with 64 output filters on a
  32x32 image
  # with `data_format="channels_last"`:
  model = Sequential()
  model.add(LocallyConnected2D(64, (3, 3), input_shape=(32, 32, 3)))
  # now model.output_shape == (None, 30, 30, 64)
  # notice that this layer will consume (30*30)*(3*3*3*64) + (30*30)*64
  parameters

  # add a 3x3 unshared weights convolution on top, with 32 output filters:
  model.add(LocallyConnected2D(32, (3, 3)))
  # now model.output_shape == (None, 28, 28, 32)
  ```

- __Arguments__:
	- __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
	- __kernel_size__: An integer or tuple/list of 2 integers, specifying the
	  width and height of the 2D convolution window.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	- __strides__: An integer or tuple/list of 2 integers,
	  specifying the strides of the convolution along the width and height.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	- __padding__: Currently only support `"valid"` (case-insensitive).
	  `"same"` will be supported in future.
	- __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, height, width, channels)` while `channels_first`
	  corresponds to inputs with shape
	  `(batch, channels, height, width)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
	  If you never set it, then it will be "channels_last".
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
	- __kernel_constraint__: Constraint function applied to the kernel matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.

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
  