<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/advanced_activations.py#L28)</span>
## LeakyReLUConfig

```python
polyaxon_schemas.layers.advanced_activations.LeakyReLUConfig(alpha=0.3)
```

Leaky version of a Rectified Linear Unit.

It allows a small gradient when the unit is not active:
`f(x) = alpha * x for x < 0`,
`f(x) = x for x >= 0`.

- __Args__:

	- __alpha__: float >= 0. Negative slope coefficient.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as the input.

Polyaxonfile usage:

```yaml
LeakyReLU:
	alpha: 0.2
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/advanced_activations.py#L79)</span>
## PReLUConfig

```python
polyaxon_schemas.layers.advanced_activations.PReLUConfig(alpha_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x104210ac8>, alpha_regularizer=None, alpha_constraint=None, shared_axes=None)
```

Parametric Rectified Linear Unit.

It follows:
`f(x) = alpha * x for x < 0`,
`f(x) = x for x >= 0`,
where `alpha` is a learned array with the same shape as x.

- __Args__:

	- __alpha_initializer__: initializer function for the weights.

	- __alpha_regularizer__: regularizer for the weights.

	- __alpha_constraint__: constraint for the weights.

	- __shared_axes__: the axes along which to share learnable

		parameters for the activation function.
		For example, if the incoming feature maps
		are from a 2D convolution
		with output shape `(batch, height, width, channels)`,
		and you wish to share parameters across space
		so that each filter only has one set of parameters,
		set `shared_axes=[1, 2]`.

Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as the input.

Polyaxonfile usage:

```yaml
PReLU:
  alpha_initializer:
	ZerosInitializer:
  alpha_regularizer:
	L2:
	 l: 0.01
  shared_axes: [1, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/advanced_activations.py#L151)</span>
## ELUConfig

```python
polyaxon_schemas.layers.advanced_activations.ELUConfig(alpha=0.1)
```

Exponential Linear Unit.

It follows:
`f(x) =  alpha * (exp(x) - 1.) for x < 0`,
`f(x) = x for x >= 0`.

- __Args__:

	- __alpha__: scale for the negative factor.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as the input.

Polyaxonfile usage:

```yaml
ELU:
  alpha:0.1
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/advanced_activations.py#L199)</span>
## ThresholdedReLUConfig

```python
polyaxon_schemas.layers.advanced_activations.ThresholdedReLUConfig(theta=1.0)
```

Thresholded Rectified Linear Unit.

It follows:
`f(x) = x for x > theta`,
`f(x) = 0 otherwise`.

- __Args__:

	- __theta__: float >= 0. Threshold location of activation.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as the input.

Polyaxonfile usage:

```yaml
ThresholdedReLU:
  theta:0.1
```
