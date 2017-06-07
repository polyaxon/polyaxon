<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L25)</span>
## Conv2d

```python
polyaxon.layers.convolutional.Conv2d(mode, num_filter, filter_size, strides=1, padding='SAME', activation='linear', bias=True, weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='Conv2D')
```

Adds a 2D convolution layer.

This operation creates a variable called 'w', representing the convolutional kernel,
that is convolved with the input. A second variable called 'b' is added to the result of
the convolution operation.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: `int` or `list of int`. Size of filters.
	- __strides__: 'int` or list of `int`. Strides of conv operation.
		- __Default__: [1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`) or None.
		- __Default__: 'linear'.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv2D'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __b__: `Variable`. Variable representing biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L121)</span>
## Conv2dTranspose

```python
polyaxon.layers.convolutional.Conv2dTranspose(mode, num_filter, filter_size, output_shape, strides=1, padding='SAME', activation='linear', bias=True, weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='Conv2DTranspose')
```

Adds a Convolution 2D Transpose.

This operation is sometimes called "deconvolution" after (Deconvolutional
- __Networks)[http__://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf], but is
actually the transpose (gradient) of `conv2d` rather than an actual
deconvolution.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: `int` or `list of int`. Size of filters.
	- __output_shape__: `list of int`. Dimensions of the output tensor.
		Can optionally include the number of conv filters.
		[new height, new width, num_filter] or [new height, new width].
	- __strides__: `int` or list of `int`. Strides of conv operation.
		- __Default__: [1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv2DTranspose'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __b__: `Variable`. Variable representing biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L256)</span>
## MaxPool2d

```python
polyaxon.layers.convolutional.MaxPool2d(mode, kernel_size, strides=None, padding='SAME', name='MaxPool2D')
```

Adds Max Pooling 2D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: 'int` or `list of int`. Pooling kernel size.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: SAME as kernel_size.
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'MaxPool2D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L285)</span>
## AvgPool2d

```python
polyaxon.layers.convolutional.AvgPool2d(mode, kernel_size, strides=None, padding='SAME', name='AvgPool2D')
```

Adds Average Pooling 2D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: 'int` or `list of int`. Pooling kernel size.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: SAME as kernel_size.
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'AvgPool2D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L314)</span>
## Upsample2d

```python
polyaxon.layers.convolutional.Upsample2d(mode, kernel_size, name='UpSample2D')
```

Adds UpSample 2D operation.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: 'int` or `list of int`. Upsampling kernel size.
	- __name__: A name for this layer (optional). Default: 'UpSample2D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L1218)</span>
## HighwayConv2d

```python
polyaxon.layers.convolutional.HighwayConv2d(mode, num_filter, filter_size, strides=1, padding='SAME', activation='linear', weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='HighwayConv2D')
```

Adds a Highway Convolution 2D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: 'int` or `list of int`. Size of filters.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: [1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv2D'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __w_t__: `Variable`. Variable representing gate weights.
	- __b__: `Variable`. Variable representing biases.
	- __b_t__: `Variable`. Variable representing gate biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L345)</span>
## Upscore

```python
polyaxon.layers.convolutional.Upscore(mode, num_classes, shape=None, kernel_size=4, strides=2, trainable=True, restore=True, name='Upscore')
```

Adds an Upscore layer.

This implements the upscore layer as used in
(Fully Convolutional Networks)[http://arxiv.org/abs/1411.4038].
The upscore layer is initialized as bilinear upsampling filter.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_classes__: `int`. Number of output feature maps.
	- __shape__: `list of int`. Dimension of the output map
		[batch_size, new height, new width]. For convinience four values
		 are allows [batch_size, new height, new width, X], where X
		 is ignored.
	- __kernel_size__: 'int` or `list of int`. Upsampling kernel size.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: [1 2 2 1].
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Upscore'.

- __Links__:
	(Fully Convolutional Networks)[http://arxiv.org/abs/1411.4038]


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L436)</span>
## Conv1d

```python
polyaxon.layers.convolutional.Conv1d(mode, num_filter, filter_size, strides=1, padding='SAME', activation='linear', bias=True, weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='Conv1D')
```

Adds a Convolution 1D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: 'int` or `list of int`. Size of filters.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: [1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv1D'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __b__: `Variable`. Variable representing biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L557)</span>
## MaxPool1d

```python
polyaxon.layers.convolutional.MaxPool1d(mode, kernel_size, strides=None, padding='SAME', name='MaxPool1D')
```

Adds Max Pooling 1D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: `int` or `list of int`. Pooling kernel size.
	- __strides__: `int` or `list of int`. Strides of conv operation.
		- __Default__: SAME as kernel_size.
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'MaxPool1D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L586)</span>
## AvgPool1d

```python
polyaxon.layers.convolutional.AvgPool1d(mode, kernel_size, strides=None, padding='SAME', name='AvgPool1D')
```

Average Pooling 1D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: `int` or `list of int`. Pooling kernel size.
	- __strides__: `int` or `list of int`. Strides of conv operation.
		- __Default__: SAME as kernel_size.
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'AvgPool1D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L1334)</span>
## HighwayConv1d

```python
polyaxon.layers.convolutional.HighwayConv1d(mode, num_filter, filter_size, strides=1, padding='SAME', activation='linear', weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='HighwayConv1D')
```

Adds a Highway Convolution 1D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: 'int` or `list of int`. Size of filters.
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		- __Default__: [1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'HighwayConv1D'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __w_t__: `Variable`. Variable representing gate weights.
	- __b__: `Variable`. Variable representing biases.
	- __b_t__: `Variable`. Variable representing gate biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L615)</span>
## Conv3d

```python
polyaxon.layers.convolutional.Conv3d(mode, num_filter, filter_size, strides=1, padding='SAME', activation='linear', bias=True, weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='Conv3D')
```

Adds Convolution 3D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: `int` or `list of int`. Size of filters.
	- __strides__: 'int` or list of `int`. Strides of conv operation.
		- __Default__: [1 1 1 1 1]. Must have strides[0] = strides[4] = 1.
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv3D'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __b__: `Variable`. Variable representing biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L710)</span>
## Conv3dTranspose

```python
polyaxon.layers.convolutional.Conv3dTranspose(mode, num_filter, filter_size, output_shape, strides=1, padding='SAME', activation='linear', bias=True, weights_init='uniform_scaling', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='Conv3DTranspose')
```

Adds Convolution 3D Transpose.

This operation is sometimes called "deconvolution" after (Deconvolutional
- __Networks)[http__://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf], but is
actually the transpose (gradient) of `conv3d` rather than an actual
deconvolution.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_filter__: `int`. The number of convolutional filters.
	- __filter_size__: `int` or `list of int`. Size of filters.
	- __output_shape__: `list of int`. Dimensions of the output tensor.
		Can optionally include the number of conv filters.
		[new depth, new height, new width, num_filter]
		or [new depth, new height, new width].
	- __strides__: `int` or list of `int`. Strides of conv operation.
		- __Default__: [1 1 1 1 1].
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'truncated_normal'.
	- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'Conv2DTranspose'.

- __Attributes__:
	- __w__: `Variable`. Variable representing filter weights.
	- __b__: `Variable`. Variable representing biases.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L847)</span>
## MaxPool3d

```python
polyaxon.layers.convolutional.MaxPool3d(mode, kernel_size, strides=1, padding='SAME', name='MaxPool3D')
```

Max Pooling 3D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: 'int` or `list of int`. Pooling kernel size.
		Must have kernel_size[0] = kernel_size[1] = 1
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		Must have strides[0] = strides[4] = 1.
		- __Default__: [1 1 1 1 1]
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'MaxPool3D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L878)</span>
## AvgPool3d

```python
polyaxon.layers.convolutional.AvgPool3d(mode, kernel_size, strides=None, padding='SAME', name='AvgPool3D')
```

Average Pooling 3D.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __kernel_size__: 'int` or `list of int`. Pooling kernel size.
		Must have kernel_size[0] = kernel_size[1] = 1
	- __strides__: 'int` or `list of int`. Strides of conv operation.
		Must have strides[0] = strides[4] = 1.
		- __Default__: [1 1 1 1 1]
	- __padding__: `str` from `"SAME", "VALID"`. Padding algo to use.
		- __Default__: 'SAME'.
	- __name__: A name for this layer (optional). Default: 'AvgPool3D'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L921)</span>
## GlobalMaxPool

```python
polyaxon.layers.convolutional.GlobalMaxPool(mode, name='GlobalMaxPool')
```

Adds a Global Max Pooling.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __name__: A name for this layer (optional). Default: 'GlobalMaxPool'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L942)</span>
## GlobalAvgPool

```python
polyaxon.layers.convolutional.GlobalAvgPool(mode, name='GlobalAvgPool')
```

Adds a Global Average Pooling.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __name__: A name for this layer (optional). Default: 'GlobalAvgPool'.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L963)</span>
## ResidualBlock

```python
polyaxon.layers.convolutional.ResidualBlock(mode, num_blocks, out_channels, downsample=False, downsample_strides=2, activation='relu', batch_norm=True, bias=True, weights_init='variance_scaling', bias_init='zeros', regularizer='l2_regularizer', scale=0.0001, trainable=True, restore=True, name='ResidualBlock')
```

Adds a Residual Block.

A residual block as described in MSRA's Deep Residual Network paper.
Full pre-activation architecture is used here.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_blocks__: `int`. Number of layer blocks.
	- __out_channels__: `int`. The number of convolutional filters of the
		convolution layers.
	- __downsample__: `bool`. If True, apply downsampling using
		'downsample_strides' for strides.
	- __downsample_strides__: `int`. The strides to use when downsampling.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __batch_norm__: `bool`. If True, apply batch normalization.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'uniform_scaling'.
	- __bias_init__: `str` (name) or `tf.Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'ShallowBottleneck'.

- __References__:
	- Deep Residual Learning for Image Recognition. Kaiming He, Xiangyu
		Zhang, Shaoqing Ren, Jian Sun. 2015.
	- Identity Mappings in Deep Residual Networks. Kaiming He, Xiangyu
		Zhang, Shaoqing Ren, Jian Sun. 2015.

- __Links__:
	- [http://arxiv.org/pdf/1512.03385v1.pdf]
		(http://arxiv.org/pdf/1512.03385v1.pdf)
	- [Identity Mappings in Deep Residual Networks]
		(https://arxiv.org/pdf/1603.05027v2.pdf)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional.py#L1085)</span>
## ResidualBottleneck

```python
polyaxon.layers.convolutional.ResidualBottleneck(mode, num_blocks, bottleneck_size, out_channels, downsample=False, downsample_strides=2, activation='relu', batch_norm=True, bias=True, weights_init='variance_scaling', bias_init='zeros', regularizer='l2_regularizer', scale=0.0001, trainable=True, restore=True, name='ResidualBottleneck')
```

Adds a Residual Bottleneck.

A residual bottleneck block as described in MSRA's Deep Residual Network
paper. Full pre-activation architecture is used here.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __num_blocks__: `int`. Number of layer blocks.
	- __bottleneck_size__: `int`. The number of convolutional filter of the
		bottleneck convolutional layer.
	- __out_channels__: `int`. The number of convolutional filters of the
		layers surrounding the bottleneck layer.
	- __downsample__: `bool`. If True, apply downsampling using
		'downsample_strides' for strides.
	- __downsample_strides__: `int`. The strides to use when downsampling.
	- __activation__: `str` (name) or `function` (returning a `Tensor`).
		- __Default__: 'linear'.
	- __batch_norm__: `bool`. If True, apply batch normalization.
	- __bias__: `bool`. If True, a bias is used.
	- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
		- __Default__: 'uniform_scaling'.
	- __bias_init__: `str` (name) or `tf.Tensor`. Bias initialization.
		- __Default__: 'zeros'.
	- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
		- __Default__: None.
	- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: A name for this layer (optional). Default: 'DeepBottleneck'.

- __References__:
	- Deep Residual Learning for Image Recognition. Kaiming He, Xiangyu
		Zhang, Shaoqing Ren, Jian Sun. 2015.
	- Identity Mappings in Deep Residual Networks. Kaiming He, Xiangyu
		Zhang, Shaoqing Ren, Jian Sun. 2015.

- __Links__:
	- [http://arxiv.org/pdf/1512.03385v1.pdf]
		(http://arxiv.org/pdf/1512.03385v1.pdf)
	- [Identity Mappings in Deep Residual Networks]
		(https://arxiv.org/pdf/1603.05027v2.pdf)
