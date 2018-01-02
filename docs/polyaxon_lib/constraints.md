<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/constraints.py#L25)</span>
## MaxNormConfig

```python
polyaxon_schemas.constraints.MaxNormConfig(max_value=2, axis=0)
```

MaxNorm weight constraint.

Constrains the weights incident to each hidden unit
to have a norm less than or equal to a desired value.

- __Args__:

	- __m__: the maximum norm for the incoming weights.

	- __axis__: integer, axis along which to calculate weight norms.

		For instance, in a `Dense` layer the weight matrix
		has shape `(input_dim, output_dim)`,
		set `axis` to `0` to constrain each weight vector
		of length `(input_dim,)`.
		In a `Conv2D` layer with `data_format="channels_last"`,
		the weight tensor has shape
		`(rows, cols, input_depth, output_depth)`,
		set `axis` to `[0, 1, 2]`
		to constrain the weights of each filter tensor of size
		`(rows, cols, input_depth)`.

- __References__:

	- [Dropout: A Simple Way to Prevent Neural Networks from Overfitting
	  Srivastava, Hinton, et al.
	  2014](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)

Polyaxonfile usage:

Using the default values

```yaml
MaxNorm:
```

Using custom values

```yaml
MaxNorm:
  max_value: 3
  axis: 0
```

Example with layer

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint: MaxNorm
```

or

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint:
	MaxNorm:
	  max_value: 3
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/constraints.py#L109)</span>
## NonNegConfig

```python
polyaxon_schemas.constraints.NonNegConfig(w)
```

Constrains the weights to be non-negative.

Polyaxonfile usage:

```yaml
NonNeg:
  w: 0.2
```

Example with layer:

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint:
	NonNeg:
	  w: 0.2
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/constraints.py#L152)</span>
## UnitNormConfig

```python
polyaxon_schemas.constraints.UnitNormConfig(axis=0)
```

Constrains the weights incident to each hidden unit to have unit norm.

- __Args__:

	- __axis__: integer, axis along which to calculate weight norms.

		For instance, in a `Dense` layer the weight matrix
		has shape `(input_dim, output_dim)`,
		set `axis` to `0` to constrain each weight vector
		of length `(input_dim,)`.
		In a `Conv2D` layer with `data_format="channels_last"`,
		the weight tensor has shape
		`(rows, cols, input_depth, output_depth)`,
		set `axis` to `[0, 1, 2]`
		to constrain the weights of each filter tensor of size
		`(rows, cols, input_depth)`.

Polyaxonfile usage:

Using the default values

```yaml
UnitNorm:
```

Using custom values

```yaml
UnitNorm:
  axis: 1
```

Example with layer

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint: UnitNorm
```

or

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint:
	UnitNorm:
	  axis: 1
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/constraints.py#L228)</span>
## MinMaxNormConfig

```python
polyaxon_schemas.constraints.MinMaxNormConfig(min_value=0.0, max_value=1.0, rate=1.0, axis=0)
```

MinMaxNorm weight constraint.

Constrains the weights incident to each hidden unit
to have the norm between a lower bound and an upper bound.

- __Args__:

	- __min_value__: the minimum norm for the incoming weights.

	- __max_value__: the maximum norm for the incoming weights.

	- __rate__: rate for enforcing the constraint: weights will be

		rescaled to yield
		`(1 - rate) * norm + rate * norm.clip(min_value, max_value)`.
		Effectively, this means that rate=1.0 stands for strict
		enforcement of the constraint, while rate<1.0 means that
		weights will be rescaled at each step to slowly move
		towards a value inside the desired interval.
	- __axis__: integer, axis along which to calculate weight norms.

		For instance, in a `Dense` layer the weight matrix
		has shape `(input_dim, output_dim)`,
		set `axis` to `0` to constrain each weight vector
		of length `(input_dim,)`.
		In a `Conv2D` layer with `dim_ordering="channels_last"`,
		the weight tensor has shape
		`(rows, cols, input_depth, output_depth)`,
		set `axis` to `[0, 1, 2]`
		to constrain the weights of each filter tensor of size
		`(rows, cols, input_depth)`.

Polyaxonfile usage:

Using the default values

```yaml
MinMaxNorm:
```

Using custom values

```yaml
MinMaxNorm:
  min_value: 0.1
  max_value: 0.8
  rate: 0.9
  axis: 0
```

Example with layer

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint: MinMaxNorm
```

or

```yaml
Conv2D:
  filters: 10
  kernel_size: 8
  kernel_constraint:
	MinMaxNorm:
	  min_value: 0.1
	  max_value: 0.8
	  rate: 0.9
	  axis: 0
```
