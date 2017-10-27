<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/rl/memories.py#L13)</span>
## Memory

```python
polyaxon.rl.memories.Memory(size=1000, batch_size=32)
```

Base Agent Memory class.

- __Args__:
	- __size__: `int`. The size of the memory.
	- __batch_size__: `int`. The batch size to return during the sampling.

- __Attributes__:
	- ___size__: `int`. The size of the memory.
	- ___batch_size__: `int`. The batch size to return during the sampling.
	- ___memory__: `deque`. Where to store the data.
	- ___counter__: `int`. Number of step stored up to size.
	- ___spec__: `list`. the list of keys corresponding to the data values stored each step.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/rl/memories.py#L80)</span>
## BatchMemory

```python
polyaxon.rl.memories.BatchMemory(batch_size=5000)
```

The batch memory buffer batch size data and clear the memory after each sample.