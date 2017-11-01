<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/constraints.py#L16)</span>
## MaxNorm

```python
polyaxon.constraints.MaxNorm(max_value=2, axis=0)
```

MaxNorm weight constraint.

  Constrains the weights incident to each hidden unit
  to have a norm less than or equal to a desired value.

  Arguments:
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

  References:
  - [Dropout: A Simple Way to Prevent Neural Networks from Overfitting
	Srivastava, Hinton, et al.
	2014](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/constraints.py#L21)</span>
## NonNeg

```python
polyaxon.constraints.NonNeg()
```

Constrains the weights to be non-negative.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/constraints.py#L26)</span>
## UnitNorm

```python
polyaxon.constraints.UnitNorm(axis=0)
```

Constrains the weights incident to each hidden unit to have unit norm.

  Arguments:
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/constraints.py#L31)</span>
## MinMaxNorm

```python
polyaxon.constraints.MinMaxNorm(min_value=0.0, max_value=1.0, rate=1.0, axis=0)
```

MinMaxNorm weight constraint.

  Constrains the weights incident to each hidden unit
  to have the norm between a lower bound and an upper bound.

  Arguments:
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
  