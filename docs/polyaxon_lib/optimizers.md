<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L64)</span>
## SGDConfig

```python
polyaxon_schemas.optimizers.SGDConfig(learning_rate=0.01, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='SGD')
```

Optimizer that implements the gradient descent algorithm.

- __Args__:

	- __learning_rate__: A Tensor or a floating point value. The learning rate to use.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: SGD
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	SGD:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	SGD: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L145)</span>
## MomentumConfig

```python
polyaxon_schemas.optimizers.MomentumConfig(learning_rate=0.001, momentum=0.9, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Momentum')
```

Optimizer that implements the Momentum.

Momentum Optimizer accepts learning rate decay. When training a model,
it is often recommended to lower the learning rate as the training
progresses. The function returns the decayed learning rate.  It is
computed as:

```python
>>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
```

- __Args__:

	- __learning_rate__: `float`. Learning rate.

	- __momentum__: `float`. Momentum.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: `str`. Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Momentum
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Momentum:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Momentum: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L238)</span>
## NestrovConfig

```python
polyaxon_schemas.optimizers.NestrovConfig(learning_rate=0.001, momentum=0.9, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, use_locking=False, global_step=None, name='Nestrov')
```

Optimizer that implements the Nesterov.

Same as Momentum optimizer but uses nestrov
See [Sutskever et. al., 2013](http://jmlr.org/proceedings/papers/v28/sutskever13.pdf)

```python
>>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
```
- __Args__:

	- __learning_rate__: `float`. Learning rate.

	- __momentum__: `float`. Momentum.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: `str`. Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Nestrov
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Nestrov:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Nestrov: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L330)</span>
## RMSPropConfig

```python
polyaxon_schemas.optimizers.RMSPropConfig(learning_rate=0.001, decay=0.9, momentum=0.0, epsilon=1e-10, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='RMSProp')
```

Optimizer that implements the RMSprop.

Maintain a moving (discounted) average of the square of gradients.
Divide gradient by the root of this average.

- __Args__:

	- __learning_rate__: `float`. learning rate.

	- __decay__: `float`. Discounting factor for the history/coming gradient.

	- __momentum__: `float`. Momentum.

	- __epsilon__: `float`. Small value to avoid zero denominator.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: RMSProp
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	RMSProp:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	RMSProp: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L425)</span>
## AdamConfig

```python
polyaxon_schemas.optimizers.AdamConfig(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Adam')
```

Optimizer that implements the Adam.

The default value of 1e-8 for epsilon might not be a good default in
general. For example, when training an Inception network on ImageNet a
current good choice is 1.0 or 0.1.

- __Args__:

	- __learning_rate__: `float`. learning rate.

	- __beta1__: `float`. The exponential decay rate for the 1st moment estimates.

	- __beta2__: `float`. The exponential decay rate for the 2nd moment estimates.

	- __epsilon__: `float`. A small constant for numerical stability.

	- __epsilon__: `float`. Small value to avoid zero denominator.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: `str`. Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Adam
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adam:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adam: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L520)</span>
## AdagradConfig

```python
polyaxon_schemas.optimizers.AdagradConfig(learning_rate=0.01, initial_accumulator_value=0.1, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Adagrad')
```

Optimizer that implements AdaGrad.

- __Args__:

	- __learning_rate__: `float`. Learning rate.

	- __initial_accumulator_value__: `float`. Starting value for the

		accumulators, must be positive.
	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: `str`. Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Adagrad
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adagrad:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adagrad: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L606)</span>
## AdadeltaConfig

```python
polyaxon_schemas.optimizers.AdadeltaConfig(learning_rate=0.99, rho=0.95, epsilon=1e-08, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Adadelta')
```

Optimizer that implements Ftrl Proximal.

The Ftrl-proximal algorithm, abbreviated for Follow-the-regularized-leader,
is described in the paper below.

It can give a good performance vs. sparsity tradeoff.

Ftrl-proximal uses its own global base learning rate and can behave like
Adagrad with `learning_rate_power=-0.5`, or like gradient descent with
`learning_rate_power=0.0`.

- __Args__:

	- __learning_rate__: `float`. Learning rate.

	- __learning_rate_power__: `float`. Must be less or equal to zero.

	- __initial_accumulator_value__: `float`. The starting value for accumulators.

		Only positive values are allowed.
	- __l1_regularization_strength__: `float`. Must be less or equal to zero.

	- __l2_regularization_strength__: `float`. Must be less or equal to zero.

	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: `str`. Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Adadelta
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adadelta:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Adadelta: {learning_rate: 0.21}
  # other model properties
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/optimizers.py#L708)</span>
## FtrlConfig

```python
polyaxon_schemas.optimizers.FtrlConfig(learning_rate=3.0, learning_rate_power=-0.5, initial_accumulator_value=0.1, l1_regularization_strength=0.0, l2_regularization_strength=0.0, decay_type='', decay_rate=0.0, decay_steps=10000, start_decay_at=0, stop_decay_at=10000000000.0, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Ftrl')
```

Optimizer that implements AdaDelta.

- __Args__:

	- __learning_rate__: A `Tensor` or a floating point value. The learning rate.

	- __rho__: A `Tensor` or a floating point value. The decay rate.

	- __epsilon__: A `Tensor` or a floating point value.  A constant epsilon used to better

		conditioning the grad update.
	- __decay_type__: A decay function name defined in `tf.train`

	- __decay_rate__: `float`. The learning rate decay to apply.

	- __decay_steps__: `int`. Apply decay every provided steps.

	- __start_decay_at__: `int`. Don't decay before this step.

	- __stop_decay_at__: `int`. Don't decay after this step.

	- __min_learning_rate__: `float`. Don't decay below this number.

	- __staircase__: `bool`. It `True` decay learning rate at discrete intervals.

	- __global_step__: Scalar int `Tensor`, step counter for each update.

	- __use_locking__: If True use locks for update operations.

	- __name__: Optional name prefix for the operations created when applying gradients.


Polyaxonfile usage:

```yaml
model:
  # other model properties
  optimizer: Ftrl
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Ftrl:
	  learning_rate: 0.21
  # other model properties
```

or

```yaml
model:
  # other model properties
  optimizer:
	Ftrl: {learning_rate: 0.21}
  # other model properties
```
