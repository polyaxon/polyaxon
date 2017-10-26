## constant


```python
constant(value=0.5)
```


Builds a constant exploration.

- __Args__:
	- __value__: `float`. The exploratoin constant to use.

- __Returns__:
	`function` the exploration function logic.


----

## greedy


```python
greedy()
```


Builds a greedy exploration. (never selects random values, i.e. random() < 0 == False).

- __Returns__:
	`function` the exploration function logic.


----

## random


```python
random()
```


Builds a random exploration (always selects random values, i.e. random() < 1 == True).

- __Returns__:
	`function` the exploration function logic.


----

## decay


```python
decay(exploration_rate=0.15, decay_type='polynomial_decay', start_decay_at=0, stop_decay_at=1000000000.0, decay_rate=0.0, staircase=False, decay_steps=100000, min_exploration_rate=0)
```


Builds a decaying exploration.

Decay epsilon based on number of states and the decay_type.

- __Args__:
	- __exploration_rate__: `float` or `list` of `float`. The initial value of the exploration rate.
	- __decay_type__: A decay function name defined in `exploration_decay`
	possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
			 piecewise_constant, polynomial_decay.
	- __start_decay_at__: `int`. When to start the decay.
	- __stop_decay_at__: `int`. When to stop the decay.
	- __decay_rate__: A Python number.  The decay rate.
	- __staircase__: Whether to apply decay in a discrete staircase,
	as opposed to continuous, fashion.
	- __decay_steps__: How often to apply decay.
	- __min_exploration_rate__: `float`. Don't decay below this number.

- __Returns__:
	`function` the exploration logic operation.


----

## random_decay


```python
random_decay(num_actions=None, decay_type='polynomial_decay', start_decay_at=0, stop_decay_at=1000000000.0, decay_rate=0.0, staircase=False, decay_steps=10000, min_exploration_rate=0)
```


Builds a random decaying exploration.

Decay a random value based on number of states and the decay_type.

- __Args__:
	- __num_actions__: `int` or None. If discrete num_action must be None.
	- __decay_type__: A decay function name defined in `exploration_decay`
	possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
			 piecewise_constant, polynomial_decay.
	- __start_decay_at__: `int`. When to start the decay.
	- __stop_decay_at__: `int`. When to stop the decay.
	- __decay_rate__: A Python number.  The decay rate.
	- __staircase__: Whether to apply decay in a discrete staircase,
	as opposed to continuous, fashion.
	- __decay_steps__: How often to apply decay.
	- __min_exploration_rate__: `float`. Don't decay below this number.

- __Returns__:
	`function` the exploration logic operation.


----

## ornsteinuhlenbeck_process


```python
ornsteinuhlenbeck_process(num_actions, sigma=0.3, mu=0, theta=0.15)
```


Builds an exploration based on the Ornstein-Uhlenbeck process

The process adds time-correlated noise to the actions taken by the deterministic policy.
The OU process satisfies the following stochastic differential equation:
`dxt = theta*(mu - xt)*dt + sigma*dWt`, where Wt denotes the Wiener process.
