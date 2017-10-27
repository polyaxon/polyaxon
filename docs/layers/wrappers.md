<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/wrappers.py#L17)</span>
## Wrapper

```python
polyaxon.layers.wrappers.Wrapper(layer)
```

Abstract wrapper base class.

  Wrappers take another layer and augment it in various ways.
  Do not use this class as a layer, it is only an abstract base class.
  Two usable wrappers are the `TimeDistributed` and `Bidirectional` wrappers.

- __Arguments__:
	- __layer__: The layer to be wrapped.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/wrappers.py#L22)</span>
## TimeDistributed

```python
polyaxon.layers.wrappers.TimeDistributed(layer)
```

This wrapper allows to apply a layer to every temporal slice of an input.

  The input should be at least 3D, and the dimension of index one
  will be considered to be the temporal dimension.

  Consider a batch of 32 samples,
  where each sample is a sequence of 10 vectors of 16 dimensions.
  The batch input shape of the layer is then `(32, 10, 16)`,
  and the `input_shape`, not including the samples dimension, is `(10, 16)`.

  You can then use `TimeDistributed` to apply a `Dense` layer
  to each of the 10 timesteps, independently:

  ```python
  # as the first layer in a model
  model = Sequential()
  model.add(TimeDistributed(Dense(8), input_shape=(10, 16)))
  # now model.output_shape == (None, 10, 8)
  ```

  The output will then have shape `(32, 10, 8)`.

  In subsequent layers, there is no need for the `input_shape`:

  ```python
  model.add(TimeDistributed(Dense(32)))
  # now model.output_shape == (None, 10, 32)
  ```

  The output will then have shape `(32, 10, 32)`.

  `TimeDistributed` can be used with arbitrary layers, not just `Dense`,
  for instance with a `Conv2D` layer:

  ```python
  model = Sequential()
  model.add(TimeDistributed(Conv2D(64, (3, 3)),
					input_shape=(10, 299, 299, 3)))
  ```

- __Arguments__:
	- __layer__: a layer instance.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/wrappers.py#L27)</span>
## Bidirectional

```python
polyaxon.layers.wrappers.Bidirectional(layer, merge_mode='concat', weights=None)
```

Bidirectional wrapper for RNNs.

- __Arguments__:
	- __layer__: `Recurrent` instance.
	- __merge_mode__: Mode by which outputs of the
	  forward and backward RNNs will be combined.
	  One of {'sum', 'mul', 'concat', 'ave', None}.
	  If None, the outputs will not be combined,
	  they will be returned as a list.

- __Raises__:
	- __ValueError__: In case of invalid `merge_mode` argument.

- __Examples__:

  ```python
  model = Sequential()
  model.add(Bidirectional(LSTM(10, return_sequences=True), input_shape=(5,
  10)))
  model.add(Bidirectional(LSTM(10)))
  model.add(Dense(5))
  model.add(Activation('softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
  ```
  