## get_global_episode


```python
get_global_episode(graph=None)
```


----

## get_or_create_global_episode


```python
get_or_create_global_episode(graph=None)
```


----

## get_global_timestep


```python
get_global_timestep(graph=None)
```


----

## create_global_episode


```python
create_global_episode(graph=None)
```


----

## get_or_create_global_timestep


```python
get_or_create_global_timestep(graph=None)
```


----

## create_global_timestep


```python
create_global_timestep(graph=None)
```


----

## get_global_counter


```python
get_global_counter(collection, name, graph=None)
```


Get the global counter tensor.

The global counter tensor must be an integer variable. We first try to find it
in the collection, or by name.

- __Args__:
	- __collection__: the counter's collection.
	- __name__: the counter's name.
	- __graph__: The graph to find the global counter in. If missing, use default graph.

- __Returns__:
	The global counter variable, or `None` if none was found.

- __Raises__:
	- __TypeError__: If the global counter tensor has a non-integer type,
	or if it is not a `Variable`.


----

## get_or_create_global_counter


```python
get_or_create_global_counter(collection, name, graph=None)
```


Returns and create (if necessary) the global counter tensor.

- __Args__:
	- __collection__: the counter's collection.
	- __name__: the counter's name.
	- __graph__: The graph in which to create the global counter tensor.
	If missing, use default graph.

- __Returns__:
	The global counter tensor.


----

## create_global_counter


```python
create_global_counter(collection, name, graph=None)
```


Create global counter tensor in graph.

- __Args__:
	- __collection__: the counter's collection.
	- __name__: the counter's name.
	- __graph__: The graph in which to create the global counter tensor. If missing,
	use default graph.

- __Returns__:
	Global step tensor.

- __Raises__:
	- __ValueError__: if global counter tensor is already defined.


----

## assert_global_counter


```python
assert_global_counter(global_counter_tensor)
```


Asserts `global_counter_tensor` is a scalar int `Variable` or `Tensor`.

- __Args__:
	- __global_counter_tensor__: `Tensor` to test.


----

## get_cumulative_rewards


```python
get_cumulative_rewards(reward, done, discount=0.99)
```


compute cumulative rewards R(s,a) (a.k.a. G(s,a) in Sutton '16)

`R_t = r_t + gamma*r_{t+1} + gamma^2*r_{t+2} + ...`

The simple way to compute cumulative rewards is to iterate from last to first time tick
and compute R_t = r_t + gamma*R_{t+1} recurrently

- __Args__:
	- __reward__: `list`. A list of immediate rewards r(s,a) for the passed episodes.
	- __done__: `list`. A list of terminal states for the passed episodes.
	- __discount__: `float`. The discount factor.


----

## conjugate_gradient


```python
conjugate_gradient(fn, b, iterations=50, residual_tolerance=1e-10)
```


Conjugate gradient solver.


- __Args__:
	- __fn__: Ax of Ax=b
	- __b__: b in Ax = b

- __Returns__: Approximate solution to linear system.


----

## line_search


```python
line_search(fn, initial_x, full_step, expected_improve_rate, max_backtracks=10, accept_ratio=0.1)
```


Backtracking line search, where expected_improve_rate is the slope dy/dx at the initial.