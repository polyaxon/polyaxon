<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L16)</span>
## Add

```python
polyaxon.layers.merge.Add()
```

Layer that adds a list of inputs.

  It takes as input a list of tensors,
  all of the same shape, and returns
  a single tensor (also of the same shape).
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L21)</span>
## Multiply

```python
polyaxon.layers.merge.Multiply()
```

Layer that multiplies (element-wise) a list of inputs.

  It takes as input a list of tensors,
  all of the same shape, and returns
  a single tensor (also of the same shape).
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L26)</span>
## Average

```python
polyaxon.layers.merge.Average()
```

Layer that averages a list of inputs.

  It takes as input a list of tensors,
  all of the same shape, and returns
  a single tensor (also of the same shape).
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L31)</span>
## Maximum

```python
polyaxon.layers.merge.Maximum()
```

Layer that computes the maximum (element-wise) a list of inputs.

  It takes as input a list of tensors,
  all of the same shape, and returns
  a single tensor (also of the same shape).
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L36)</span>
## Concatenate

```python
polyaxon.layers.merge.Concatenate(axis=-1)
```

Layer that concatenates a list of inputs.

  It takes as input a list of tensors,
  all of the same shape expect for the concatenation axis,
  and returns a single tensor, the concatenation of all inputs.

- __Arguments__:
	- __axis__: Axis along which to concatenate.
	- __**kwargs__: standard layer keyword arguments.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/merge.py#L41)</span>
## Dot

```python
polyaxon.layers.merge.Dot(axes, normalize=False)
```

Layer that computes a dot product between samples in two tensors.

  E.g. if applied to two tensors `a` and `b` of shape `(batch_size, n)`,
  the output will be a tensor of shape `(batch_size, 1)`
  where each entry `i` will be the dot product between
  `a[i]` and `b[i]`.

- __Arguments__:
	- __axes__: Integer or tuple of integers,
	  axis or axes along which to take the dot product.
	- __normalize__: Whether to L2-normalize samples along the
	  dot product axis before taking the dot product.
	  If set to True, then the output of the dot product
	  is the cosine proximity between the two samples.
	- __**kwargs__: Standard layer keyword arguments.
  