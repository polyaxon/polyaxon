### adadelta


```python
adadelta(learning_rate=0.001, rho=0.1, epsilon=1e-08, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='AdaDelta')
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

----

### create_learning_rate_decay_fn


```python
create_learning_rate_decay_fn(learning_rate, decay_type, decay_steps, decay_rate, start_decay_at=0, stop_decay_at=1000000000.0, min_learning_rate=None, staircase=False, global_step=None)
```


Creates a function that decays the learning rate.

- __Args__:
- __learning_rate__: A Tensor or a floating point value. The learning rate to use.
- __decay_steps__: How often to apply decay.
- __decay_rate__: A Python number. The decay rate.
- __start_decay_at__: Don't decay before this step
- __stop_decay_at__: Don't decay after this step
- __min_learning_rate__: Don't decay below this number
- __decay_type__: A decay function name defined in `tf.train`
possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
		 piecewise_constant, polynomial_decay.
- __staircase__: Whether to apply decay in a discrete staircase,
as opposed to continuous, fashion.
- __global_step__: Scalar int `Tensor`, step counter for each update. If not supplied,
it will be fetched from the default graph (see `tf.contrib.framework.get_global_step`
for details). If it's not been created, no step will be incremented with each weight
update. `learning_rate_decay_fn` requires `global_step`.

- __Returns__:
A function that takes (learning_rate, global_step) as inputs
and returns the learning rate for the given step.
Returns `None` if decay_type is empty or None.

----

### sgd


```python
sgd(learning_rate=0.001, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='SGD')
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

----

### momentum


```python
momentum(learning_rate=0.001, momentum=0.9, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Momentum')
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

----

### nesterov


```python
nesterov(learning_rate=0.001, momentum=0.9, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, use_locking=False, global_step=None, name='Momentum')
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

----

### rmsprop


```python
rmsprop(learning_rate=0.001, decay=0.9, momentum=0.0, epsilon=1e-10, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='RMSProp')
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

----

### adam


```python
adam(learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-08, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Adam')
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

----

### adagrad


```python
adagrad(learning_rate=0.001, initial_accumulator_value=0.1, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='AdaGrad')
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

----

### ftrl


```python
ftrl(learning_rate=3.0, learning_rate_power=-0.5, initial_accumulator_value=0.1, l1_regularization_strength=0.0, l2_regularization_strength=0.0, decay_type='', decay_rate=0.0, decay_steps=100, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, global_step=None, use_locking=False, name='Ftrl')
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
- __name__: `str`. Optional name prefix for the operations created when applying gradients..
