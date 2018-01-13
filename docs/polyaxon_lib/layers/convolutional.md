<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L46)</span>
## Conv1DConfig

```python
polyaxon_schemas.layers.convolutional.Conv1DConfig(filters, kernel_size, strides=1, padding='valid', dilation_rate=1, activation=None, use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f57c50>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f57c18>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
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

- __Args__:

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

Polyaxon usage:

```yaml
Conv1D:
  filters: 10
  kernel_size: 3
  strides: 1
  padding: same
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L179)</span>
## Conv2DConfig

```python
polyaxon_schemas.layers.convolutional.Conv2DConfig(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), activation=None, use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f622b0>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f62278>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
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

- __Args__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L358)</span>
## Conv3DConfig

```python
polyaxon_schemas.layers.convolutional.Conv3DConfig(filters, kernel_size, strides=(1, 1, 1), padding='valid', data_format=None, dilation_rate=(1, 1, 1), activation=None, use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f628d0>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f62898>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
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

- __Args__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L516)</span>
## Conv2DTransposeConfig

```python
polyaxon_schemas.layers.convolutional.Conv2DTransposeConfig(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), activation=None, use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f62ef0>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f62eb8>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
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

- __Args__:

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

- __References__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L671)</span>
## Conv3DTransposeConfig

```python
polyaxon_schemas.layers.convolutional.Conv3DTransposeConfig(filters, kernel_size, strides=(1, 1, 1), padding='valid', data_format=None, activation=None, dilation_rate=(1, 1, 1), use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f71550>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f71518>, kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)
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

- __Args__:

	- __filters__: Integer, the dimensionality of the output space

		(i.e. the number of output filters in the convolution).
	- __kernel_size__: An integer or tuple/list of 3 integers, specifying the

		depth, height and width of the 3D convolution window.
		Can be a single integer to specify the same value for
		all spatial dimensions.
	- __strides__: An integer or tuple/list of 3 integers,

		specifying the strides of the convolution along the depth, height
		  and width.
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
		If you never set it, then it will be "channels_last".
	- __dilation_rate__: an integer or tuple/list of 3 integers, specifying

		the dilation rate to use for dilated convolution.
		Can be a single integer to specify the same value for
		all spatial dimensions.
		Currently, specifying any `dilation_rate` value != 1 is
		incompatible with specifying any stride value != 1.
	- __activation__: Activation function to use

		If you don't specify anything, no activation is applied
		(ie. "linear" activation: `a(x) = x`).
	- __use_bias__: Boolean, whether the layer uses a bias vector.

	- __kernel_initializer__: Initializer for the `kernel` weights matrix

	- __bias_initializer__: Initializer for the bias vector

	- __kernel_regularizer__: Regularizer function applied to

		the `kernel` weights matrix
	- __bias_regularizer__: Regularizer function applied to the bias vector

	- __activity_regularizer__: Regularizer function applied to

		the output of the layer (its "activation").
	- __kernel_constraint__: Constraint function applied to the kernel matrix

	- __bias_constraint__: Constraint function applied to the bias vector


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

- __References__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L831)</span>
## SeparableConv2DConfig

```python
polyaxon_schemas.layers.convolutional.SeparableConv2DConfig(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, depth_multiplier=1, activation=None, use_bias=True, depthwise_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f71be0>, pointwise_initializer=<polyaxon_schemas.initializations.GlorotNormalInitializerConfig object at 0x101f71ba8>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x101f71c18>, depthwise_regularizer=None, pointwise_regularizer=None, bias_regularizer=None, activity_regularizer=None, depthwise_constraint=None, pointwise_constraint=None, bias_constraint=None)
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

- __Args__:

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

		the pointwise kernel matrix.
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

Polyaxonfile usage:

```yaml
SeparableConv2D:
  filters: 10
  kernel_size: 2 or [2, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L971)</span>
## UpSampling1DConfig

```python
polyaxon_schemas.layers.convolutional.UpSampling1DConfig(size=2)
```

Upsampling layer for 1D inputs.

Repeats each temporal step `size` times along the time axis.

- __Args__:

	- __size__: integer. Upsampling factor.


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1029)</span>
## UpSampling2DConfig

```python
polyaxon_schemas.layers.convolutional.UpSampling2DConfig(size=(2, 2), data_format=None)
```

Upsampling layer for 2D inputs.

Repeats the rows and columns of the data
by size[0] and size[1] respectively.

- __Args__:

	- __size__: int, or tuple of 2 integers.

		The upsampling factors for rows and columns.
	- __data_format__: A string,

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1100)</span>
## UpSampling3DConfig

```python
polyaxon_schemas.layers.convolutional.UpSampling3DConfig(size=(2, 2, 2), data_format=None)
```

Upsampling layer for 3D inputs.

Repeats the 1st, 2nd and 3rd dimensions
of the data by size[0], size[1] and size[2] respectively.

- __Args__:

	- __size__: int, or tuple of 3 integers.

		The upsampling factors for dim1, dim2 and dim3.
	- __data_format__: A string,

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1169)</span>
## ZeroPadding1DConfig

```python
polyaxon_schemas.layers.convolutional.ZeroPadding1DConfig(padding=1)
```

Zero-padding layer for 1D input (e.g. temporal sequence).

- __Args__:

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

Polyaxonfile usage:

```yaml
ZeroPadding1D:
```

or

```yaml
ZeroPadding1D:
	padding: 1
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1225)</span>
## ZeroPadding2DConfig

```python
polyaxon_schemas.layers.convolutional.ZeroPadding2DConfig(padding=(1, 1), data_format=None)
```

Zero-padding layer for 2D input (e.g. picture).

This layer can add rows and columns of zeros
at the top, bottom, left and right side of an image tensor.

- __Args__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1304)</span>
## ZeroPadding3DConfig

```python
polyaxon_schemas.layers.convolutional.ZeroPadding3DConfig(padding=(1, 1, 1), data_format=None)
```

Zero-padding layer for 3D data (spatial or spatio-temporal).

- __Args__:

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1383)</span>
## Cropping1DConfig

```python
polyaxon_schemas.layers.convolutional.Cropping1DConfig(cropping=(1, 1))
```

Cropping layer for 1D input (e.g. temporal sequence).

It crops along the time dimension (axis 1).

- __Args__:

	- __cropping__: int or tuple of int (length 2)

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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1440)</span>
## Cropping2DConfig

```python
polyaxon_schemas.layers.convolutional.Cropping2DConfig(cropping=((0, 0), (0, 0)), data_format=None)
```

Cropping layer for 2D input (e.g. picture).

It crops along spatial dimensions, i.e. width and height.

- __Args__:

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

- __Example__:


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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/convolutional.py#L1525)</span>
## Cropping3DConfig

```python
polyaxon_schemas.layers.convolutional.Cropping3DConfig(cropping=((1, 1), (1, 1), (1, 1)), data_format=None)
```

Cropping layer for 3D data (e.g.

spatial or spatio-temporal).

- __Args__:

	- __cropping__: int, or tuple of 23ints, or tuple of 3 tuples of 2 ints.

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
	- __data_format__: A string,

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
