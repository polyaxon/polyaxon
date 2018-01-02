<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L25)</span>
## AddConfig

```python
polyaxon_schemas.layers.merge.AddConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Layer that adds a list of inputs.

It takes as input a list of tensors,
all of the same shape, and returns
a single tensor (also of the same shape).

Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Add:
	  inbound_nodes: [dense1, dense2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L121)</span>
## MultiplyConfig

```python
polyaxon_schemas.layers.merge.MultiplyConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Layer that multiplies (element-wise) a list of inputs.

It takes as input a list of tensors,
all of the same shape, and returns
a single tensor (also of the same shape).

Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Multiply:
	  inbound_nodes: [dense1, dense2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L164)</span>
## AverageConfig

```python
polyaxon_schemas.layers.merge.AverageConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Layer that averages a list of inputs.

It takes as input a list of tensors,
all of the same shape, and returns
a single tensor (also of the same shape).

Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Average:
	  inbound_nodes: [dense1, dense2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L207)</span>
## MaximumConfig

```python
polyaxon_schemas.layers.merge.MaximumConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Layer that computes the maximum (element-wise) a list of inputs.

It takes as input a list of tensors,
all of the same shape, and returns
a single tensor (also of the same shape).

Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Maximum:
	  inbound_nodes: [dense1, dense2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L251)</span>
## ConcatenateConfig

```python
polyaxon_schemas.layers.merge.ConcatenateConfig(axis=-1)
```

Layer that concatenates a list of inputs.

It takes as input a list of tensors,
all of the same shape expect for the concatenation axis,
and returns a single tensor, the concatenation of all inputs.

- __Args__:

	- __axis__: Axis along which to concatenate.

	- __**kwargs__: standard layer keyword arguments.


Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Concatenate:
	  axis: 1
	  inbound_nodes: [dense1, dense2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/merge.py#L305)</span>
## DotConfig

```python
polyaxon_schemas.layers.merge.DotConfig(axes, normalize=False)
```

Layer that computes a dot product between samples in two tensors.

E.g. if applied to two tensors `a` and `b` of shape `(batch_size, n)`,
the output will be a tensor of shape `(batch_size, 1)`
where each entry `i` will be the dot product between
`a[i]` and `b[i]`.

- __Args__:

	- __axes__: Integer or tuple of integers,

		axis or axes along which to take the dot product.
	- __normalize__: Whether to L2-normalize samples along the

		dot product axis before taking the dot product.
		If set to True, then the output of the dot product
		is the cosine proximity between the two samples.
	- __**kwargs__: Standard layer keyword arguments.


Polyaxonfile usage:

```yaml
- Dense:
	units: 10
	activation: softmax
	name: dense1

- Dense:
	units: 10
	activation: softmax
	name: dense2

- Merge:
	Dot:
	  axes: [1, 2]
	  inbound_nodes: [dense1, dense2]
```
