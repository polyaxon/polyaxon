<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L30)</span>
## Conv1D

```python
polyaxon.layers.convolutional.Conv1D(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

1D convolution layer (e.g. temporal convolution).

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

  Arguments:
  - __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
  - __kernel_size__: An integer or tuple/list of a single integer,
	  specifying the length of the 1D convolution window.
  - __strides__: An integer or tuple/list of a single integer,
	  specifying the stride length of the convolution.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: One of `"valid"`, `"causal"` or `"same"` (case-insensitive).
	  `"causal"` results in causal (dilated) convolutions, e.g. output[t]
	  does not depend on input[t+1:]. Useful when modeling temporal data
	  where the model should not violate the temporal order.
	  See [WaveNet: A Generative Model for Raw Audio, section
		2.1](https://arxiv.org/abs/1609.03499).
  - __dilation_rate__: an integer or tuple/list of a single integer, specifying
	  the dilation rate to use for dilated convolution.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any `strides` value != 1.
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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L69)</span>
## Conv2D

```python
polyaxon.layers.convolutional.Conv2D(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

2D convolution layer (e.g. spatial convolution over images).

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

  Arguments:
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
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: one of `"valid"` or `"same"` (case-insensitive).
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
  - __dilation_rate__: an integer or tuple/list of 2 integers, specifying
	  the dilation rate to use for dilated convolution.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any stride value != 1.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L109)</span>
## Conv3D

```python
polyaxon.layers.convolutional.Conv3D(filters, kernel_size, strides=(1, 1, 1), padding='valid', data_format=None, dilation_rate=(1, 1, 1), activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

3D convolution layer (e.g. spatial convolution over volumes).

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

  Arguments:
  - __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
  - __kernel_size__: An integer or tuple/list of 3 integers, specifying the
	  depth, height and width of the 3D convolution window.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
  - __strides__: An integer or tuple/list of 3 integers,
	  specifying the strides of the convolution along each spatial
		dimension.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: one of `"valid"` or `"same"` (case-insensitive).
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
	  If you never set it, then it will be "channels_last".
  - __dilation_rate__: an integer or tuple/list of 3 integers, specifying
	  the dilation rate to use for dilated convolution.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any stride value != 1.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L149)</span>
## Conv2DTranspose

```python
polyaxon.layers.convolutional.Conv2DTranspose(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Transposed convolution layer (sometimes called Deconvolution).

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

  Arguments:
  - __filters__: Integer, the dimensionality of the output space
	  (i.e. the number of output filters in the convolution).
  - __kernel_size__: An integer or tuple/list of 2 integers, specifying the
	  width and height of the 2D convolution window.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
  - __strides__: An integer or tuple/list of 2 integers,
	  specifying the strides of the convolution along the width and height.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: one of `"valid"` or `"same"` (case-insensitive).
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
  - __dilation_rate__: an integer or tuple/list of 2 integers, specifying
	  the dilation rate to use for dilated convolution.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any stride value != 1.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L187)</span>
## Conv3DTranspose

```python
polyaxon.layers.convolutional.Conv3DTranspose(filters, kernel_size, strides=(1, 1, 1), padding='valid', data_format=None, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
```

Transposed convolution layer (sometimes called Deconvolution).

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

  Arguments:
  - __filters__: Integer, the dimensionality of the output space
	  (i.e. the number of output filters in the convolution).
  - __kernel_size__: An integer or tuple/list of 3 integers, specifying the
	  width and height of the 3D convolution window.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
  - __strides__: An integer or tuple/list of 3 integers,
	  specifying the strides of the convolution along the width and height.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: one of `"valid"` or `"same"` (case-insensitive).
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, depth, height, width, channels)` while `channels_first`
	  corresponds to inputs with shape
	  `(batch, channels, depth, height, width)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
	  If you never set it, then it will be "channels_last".
  - __dilation_rate__: an integer or tuple/list of 3 integers, specifying
	  the dilation rate to use for dilated convolution.
	  Can be a single integer to specify the same value for
	  all spatial dimensions.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any stride value != 1.
  - __activation__: Activation function to use
	  (see [activations](../activations.md)).
	  If you don't specify anything, no activation is applied
	  (ie. "linear" activation: `a(x) = x`).
  - __use_bias__: Boolean, whether the layer uses a bias vector.
  - __kernel_initializer__: Initializer for the `kernel` weights matrix
	  (see [initializers](../initializers.md)).
  - __bias_initializer__: Initializer for the bias vector
	  (see [initializers](../initializers.md)).
  - __kernel_regularizer__: Regularizer function applied to
	  the `kernel` weights matrix
	  (see [regularizer](../regularizers.md)).
  - __bias_regularizer__: Regularizer function applied to the bias vector
	  (see [regularizer](../regularizers.md)).
  - __activity_regularizer__: Regularizer function applied to
	  the output of the layer (its "activation").
	  (see [regularizer](../regularizers.md)).
  - __kernel_constraint__: Constraint function applied to the kernel matrix
	  (see [constraints](../constraints.md)).
  - __bias_constraint__: Constraint function applied to the bias vector
	  (see [constraints](../constraints.md)).

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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L225)</span>
## SeparableConv2D

```python
polyaxon.layers.convolutional.SeparableConv2D(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, depth_multiplier=1, activation=None, use_bias=True, depthwise_initializer='glorot_uniform', pointwise_initializer='glorot_uniform', bias_initializer='zeros', depthwise_regularizer=None, pointwise_regularizer=None, bias_regularizer=None, activity_regularizer=None, depthwise_constraint=None, pointwise_constraint=None, bias_constraint=None)
```

Depthwise separable 2D convolution.

  Separable convolutions consist in first performing
  a depthwise spatial convolution
  (which acts on each input channel separately)
  followed by a pointwise convolution which mixes together the resulting
  output channels. The `depth_multiplier` argument controls how many
  output channels are generated per input channel in the depthwise step.

  Intuitively, separable convolutions can be understood as
  a way to factorize a convolution kernel into two smaller kernels,
  or as an extreme version of an Inception block.

  Arguments:
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
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
  - __padding__: one of `"valid"` or `"same"` (case-insensitive).
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
  - __depth_multiplier__: The number of depthwise convolution output channels
	  for each input channel.
	  The total number of depthwise convolution output
	  channels will be equal to `filterss_in * depth_multiplier`.
  - __activation__: Activation function to use.
	  If you don't specify anything, no activation is applied
	  (ie. "linear" activation: `a(x) = x`).
  - __use_bias__: Boolean, whether the layer uses a bias vector.
  - __depthwise_initializer__: Initializer for the depthwise kernel matrix.
  - __pointwise_initializer__: Initializer for the pointwise kernel matrix.
  - __bias_initializer__: Initializer for the bias vector.
  - __depthwise_regularizer__: Regularizer function applied to
	  the depthwise kernel matrix.
  - __pointwise_regularizer__: Regularizer function applied to
	  the depthwise kernel matrix.
  - __bias_regularizer__: Regularizer function applied to the bias vector.
  - __activity_regularizer__: Regularizer function applied to
	  the output of the layer (its "activation")..
  - __depthwise_constraint__: Constraint function applied to
	  the depthwise kernel matrix.
  - __pointwise_constraint__: Constraint function applied to
	  the pointwise kernel matrix.
  - __bias_constraint__: Constraint function applied to the bias vector.

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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L271)</span>
## UpSampling1D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.UpSampling1D(size=2)
```

Upsampling layer for 1D inputs.

  Repeats each temporal step `size` times along the time axis.

  Arguments:
  - __size__: integer. Upsampling factor.

  Input shape:
  3D tensor with shape: `(batch, steps, features)`.

  Output shape:
  3D tensor with shape: `(batch, upsampled_steps, features)`.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L276)</span>
## UpSampling2D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.UpSampling2D(size=(2, 2), data_format=None)
```

Upsampling layer for 2D inputs.

  Repeats the rows and columns of the data
  by size[0] and size[1] respectively.

  Arguments:
  - __size__: int, or tuple of 2 integers.
	  The upsampling factors for rows and columns.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L281)</span>
## UpSampling3D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.UpSampling3D(size=(2, 2, 2), data_format=None)
```

Upsampling layer for 3D inputs.

  Repeats the 1st, 2nd and 3rd dimensions
  of the data by size[0], size[1] and size[2] respectively.

  Arguments:
  - __size__: int, or tuple of 3 integers.
	  The upsampling factors for dim1, dim2 and dim3.
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L286)</span>
## ZeroPadding1D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.ZeroPadding1D(padding=1)
```

Zero-padding layer for 1D input (e.g. temporal sequence).

  Arguments:
  - __padding__: int, or tuple of int (length 2), or dictionary.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L291)</span>
## ZeroPadding2D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.ZeroPadding2D(padding=(1, 1), data_format=None)
```

Zero-padding layer for 2D input (e.g. picture).

  This layer can add rows and columns of zeros
  at the top, bottom, left and right side of an image tensor.

  Arguments:
  - __padding__: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
	  - If int: the same symmetric padding
		  is applied to width and height.
	  - If tuple of 2 ints:
		  interpreted as two different
		  symmetric padding values for height and width:
		  `(symmetric_height_pad, symmetric_width_pad)`.
	  - If tuple of 2 tuples of 2 ints:
		  interpreted as
		  `((top_pad, bottom_pad), (left_pad, right_pad))`
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L296)</span>
## ZeroPadding3D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.ZeroPadding3D(padding=(1, 1, 1), data_format=None)
```

Zero-padding layer for 3D data (spatial or spatio-temporal).

  Arguments:
  - __padding__: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
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
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L301)</span>
## Cropping1D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.Cropping1D(cropping=(1, 1))
```

Cropping layer for 1D input (e.g. temporal sequence).

  It crops along the time dimension (axis 1).

  Arguments:
  - __cropping__: int or tuple of int (length 2)
	  How many units should be trimmed off at the beginning and end of
	  the cropping dimension (axis 1).
	  If a single int is provided,
	  the same value will be used for both.

  Input shape:
  3D tensor with shape `(batch, axis_to_crop, features)`

  Output shape:
  3D tensor with shape `(batch, cropped_axis, features)`
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L306)</span>
## Cropping2D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.Cropping2D(cropping=((0, 0), (0, 0)), data_format=None)
```

Cropping layer for 2D input (e.g. picture).

  It crops along spatial dimensions, i.e. width and height.

  Arguments:
  - __cropping__: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
	  - If int: the same symmetric cropping
		  is applied to width and height.
	  - If tuple of 2 ints:
		  interpreted as two different
		  symmetric cropping values for height and width:
		  `(symmetric_height_crop, symmetric_width_crop)`.
	  - If tuple of 2 tuples of 2 ints:
		  interpreted as
		  `((top_crop, bottom_crop), (left_crop, right_crop))`
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

  Examples:

  ```python
  # Crop the input 2D images or feature maps
  model = Sequential()
  model.add(Cropping2D(cropping=((2, 2), (4, 4)),
				   input_shape=(28, 28, 3)))
  # now model.output_shape == (None, 24, 20, 3)
  model.add(Conv2D(64, (3, 3), padding='same))
  model.add(Cropping2D(cropping=((2, 2), (2, 2))))
  # now model.output_shape == (None, 20, 16. 64)
  ```
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L311)</span>
## Cropping3D

```python
tensorflow.contrib.keras.python.keras.layers.convolutional.Cropping3D(cropping=((1, 1), (1, 1), (1, 1)), data_format=None)
```

Cropping layer for 3D data (e.g.

  spatial or spatio-temporal).

  Arguments:
  - __cropping__: int, or tuple of 2 ints, or tuple of 2 tuples of 2 ints.
	  - If int: the same symmetric cropping
		  is applied to width and height.
	  - If tuple of 2 ints:
		  interpreted as two different
		  symmetric cropping values for height and width:
		  `(symmetric_dim1_crop, symmetric_dim2_crop, symmetric_dim3_crop)`.
	  - If tuple of 2 tuples of 2 ints:
		  interpreted as
		  `((left_dim1_crop, right_dim1_crop), (left_dim2_crop,
		right_dim2_crop), (left_dim3_crop, right_dim3_crop))`
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  