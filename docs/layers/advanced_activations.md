<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/advanced_activations.py#L19)</span>
## LeakyReLU

```python
polyaxon.layers.advanced_activations.LeakyReLU(alpha=0.3)
```

Leaky version of a Rectified Linear Unit.

  It allows a small gradient when the unit is not active:
  `f(x) = alpha * x for x < 0`,
  `f(x) = x for x >= 0`.

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as the input.

- __Arguments__:
	- __alpha__: float >= 0. Negative slope coefficient.

  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/advanced_activations.py#L24)</span>
## PReLU

```python
polyaxon.layers.advanced_activations.PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=None)
```

Parametric Rectified Linear Unit.

  It follows:
  `f(x) = alpha * x for x < 0`,
  `f(x) = x for x >= 0`,
  where `alpha` is a learned array with the same shape as x.

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as the input.

- __Arguments__:
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

  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/advanced_activations.py#L29)</span>
## ELU

```python
polyaxon.layers.advanced_activations.ELU(alpha=1.0)
```

Exponential Linear Unit.

  It follows:
  `f(x) =  alpha * (exp(x) - 1.) for x < 0`,
  `f(x) = x for x >= 0`.

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as the input.

- __Arguments__:
	- __alpha__: scale for the negative factor.

  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/advanced_activations.py#L34)</span>
## ThresholdedReLU

```python
polyaxon.layers.advanced_activations.ThresholdedReLU(theta=1.0)
```

Thresholded Rectified Linear Unit.

  It follows:
  `f(x) = x for x > theta`,
  `f(x) = 0 otherwise`.

  Input shape:
  Arbitrary. Use the keyword argument `input_shape`
  (tuple of integers, does not include the samples axis)
  when using this layer as the first layer in a model.

  Output shape:
  Same shape as the input.

- __Arguments__:
	- __theta__: float >= 0. Threshold location of activation.

  