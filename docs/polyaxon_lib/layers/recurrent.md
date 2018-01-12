<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/recurrent.py#L38)</span>
## RecurrentConfig

```python
polyaxon_schemas.layers.recurrent.RecurrentConfig(return_sequences=False, return_state=False, go_backwards=False, stateful=False, unroll=False, implementation=0)
```

Abstract base class for recurrent layers.

Do not use in a model -- it's not a valid layer!
Use its children classes `LSTM`, `GRU` and `SimpleRNN` instead.

All recurrent layers (`LSTM`, `GRU`, `SimpleRNN`) also
follow the specifications of this class and accept
the keyword arguments listed below.

- __Example__:


```python
	# as the first layer in a Sequential model
	model = Sequential()
	model.add(LSTM(32, input_shape=(10, 64)))
	# now model.output_shape == (None, 32)
	# note: `None` is the batch dimension.

	# for subsequent layers, no need to specify the input size:
	model.add(LSTM(16))

	# to stack recurrent layers, you must use return_sequences=True
	# on any recurrent layer that feeds into another recurrent layer.
	# note that you only need to specify the input size on the first layer.
	model = Sequential()
	model.add(LSTM(64, input_dim=64, input_length=10, return_sequences=True))
	model.add(LSTM(32, return_sequences=True))
	model.add(LSTM(10))
```

- __Args__:

	- __weights__: list of Numpy arrays to set as initial weights.

		The list should have 3 elements, of shapes:
		`[(input_dim, output_dim), (output_dim, output_dim), (output_dim,)]`.
	- __return_sequences__: Boolean. Whether to return the last output

		in the output sequence, or the full sequence.
	- __return_state__: Boolean. Whether to return the last state

		in addition to the output.
	- __go_backwards__: Boolean (default False).

		If True, process the input sequence backwards and return the
		reversed sequence.
	- __stateful__: Boolean (default False). If True, the last state

		for each sample at index i in a batch will be used as initial
		state for the sample of index i in the following batch.
	- __unroll__: Boolean (default False).

		If True, the network will be unrolled,
		else a symbolic loop will be used.
		Unrolling can speed-up a RNN,
		although it tends to be more memory-intensive.
		Unrolling is only suitable for short sequences.
	- __implementation__: one of {0, 1, or 2}.

		If set to 0, the RNN will use
		an implementation that uses fewer, larger matrix products,
		thus running faster on CPU but consuming more memory.
		If set to 1, the RNN will use more matrix products,
		but smaller ones, thus running slower
		(may actually be faster on GPU) while consuming less memory.
		If set to 2 (LSTM/GRU only),
		the RNN will combine the input gate,
		the forget gate and the output gate into a single matrix,
		enabling more time-efficient parallelization on the GPU.
		- __Note__: RNN dropout must be shared for all gates,

		resulting in a slightly reduced regularization.
	- __input_dim__: dimensionality of the input (integer).

		This argument (or alternatively, the keyword argument `input_shape`)
		is required when using this layer as the first layer in a model.
	- __input_length__: Length of input sequences, to be specified

		when it is constant.
		This argument is required if you are going to connect
		`Flatten` then `Dense` layers upstream
		(without it, the shape of the dense outputs cannot be computed).
		Note that if the recurrent layer is not the first layer
		in your model, you would need to specify the input length
		at the level of the first layer
		(e.g. via the `input_shape` argument)

Input shape:s
	3D tensor with shape `(batch_size, timesteps, input_dim)`,
	(Optional) 2D tensors with shape `(batch_size, output_dim)`.

Output shape:
	- if `return_state`: a list of tensors. The first tensor is
		the output. The remaining tensors are the last states,
		each with shape `(batch_size, units)`.
	- if `return_sequences`: 3D tensor with shape
		`(batch_size, timesteps, units)`.
	- else, 2D tensor with shape `(batch_size, units)`.

# Masking
	This layer supports masking for input data with a variable number
	of timesteps. To introduce masks to your data,
	use an `Embedding` layer with the `mask_zero` parameter
	set to `True`.

# Note on using statefulness in RNNs
	You can set RNN layers to be 'stateful', which means that the states
	computed for the samples in one batch will be reused as initial states
	for the samples in the next batch. This assumes a one-to-one mapping
	between samples in different successive batches.

	To enable statefulness:
		- specify `stateful=True` in the layer constructor.
		- specify a fixed batch size for your model, by passing
			if sequential model:
			  `batch_input_shape=(...)` to the first layer in your model.
			else for functional model with 1 or more Input layers:
			  `batch_shape=(...)` to all the first layers in your model.
			This is the expected shape of your inputs
			*including the batch size*.
			It should be a tuple of integers, e.g. `(32, 10, 100)`.
		- specify `shuffle=False` when calling fit().

	To reset the states of your model, call `.reset_states()` on either
	a specific layer, or on your entire model.

# Note on specifying the initial state of RNNs
	You can specify the initial state of RNN layers symbolically by
	calling them with the keyword argument `initial_state`. The value of
	`initial_state` should be a tensor or list of tensors representing
	the initial state of the RNN layer.

	You can specify the initial state of RNN layers numerically by
	calling `reset_states` with the keyword argument `states`. The value of
	`states` should be a numpy array or list of numpy arrays representing
	the initial state of the RNN layer.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/recurrent.py#L214)</span>
## SimpleRNNConfig

```python
polyaxon_schemas.layers.recurrent.SimpleRNNConfig(units, activation='tanh', use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotUniformInitializerConfig object at 0x10774e9e8>, recurrent_initializer=<polyaxon_schemas.initializations.OrthogonalInitializerConfig object at 0x10774e9b0>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x10774ea20>, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Fully-connected RNN where the output is to be fed back to input.

- __Args__:

	- __units__: Positive integer, dimensionality of the output space.

	- __activation__: Activation function to use.

		If you don't specify anything, no activation is applied
		If you pass None, no activation is applied
		(ie. "linear" activation: `a(x) = x`).
	- __use_bias__: Boolean, whether the layer uses a bias vector.

	- __kernel_initializer__: Initializer for the `kernel` weights matrix,

		used for the linear transformation of the inputs..
	- __recurrent_initializer__: Initializer for the `recurrent_kernel`

		weights matrix,
		used for the linear transformation of the recurrent state..
	- __bias_initializer__: Initializer for the bias vector.

	- __kernel_regularizer__: Regularizer function applied to

		the `kernel` weights matrix.
	- __recurrent_regularizer__: Regularizer function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_regularizer__: Regularizer function applied to the bias vector.

	- __activity_regularizer__: Regularizer function applied to

		the output of the layer (its "activation")..
	- __kernel_constraint__: Constraint function applied to

		the `kernel` weights matrix.
	- __recurrent_constraint__: Constraint function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.

	- __dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the inputs.
	- __recurrent_dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the recurrent state.

- __References__:

	- [A Theoretically Grounded Application of Dropout in Recurrent Neural
	  Networks](http://arxiv.org/abs/1512.05287)

Polyaxonfile usage:

```yaml
SimpleRNN:
  units: 3
  activation: tanh
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/recurrent.py#L454)</span>
## LSTMConfig

```python
polyaxon_schemas.layers.recurrent.LSTMConfig(units, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotUniformInitializerConfig object at 0x1077765c0>, recurrent_initializer=<class 'polyaxon_schemas.initializations.OrthogonalInitializerConfig'>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x107776588>, unit_forget_bias=True, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Long-Short Term Memory unit - Hochreiter 1997.

For a step-by-step description of the algorithm, see
[this tutorial](http://deeplearning.net/tutorial/lstm.html).

- __Args__:

	- __units__: Positive integer, dimensionality of the output space.

	- __activation__: Activation function to use.

		If you pass None, no activation is applied
		(ie. "linear" activation: `a(x) = x`).
	- __recurrent_activation__: Activation function to use

		for the recurrent step.
	- __use_bias__: Boolean, whether the layer uses a bias vector.

	- __kernel_initializer__: Initializer for the `kernel` weights matrix,

		used for the linear transformation of the inputs..
	- __recurrent_initializer__: Initializer for the `recurrent_kernel`

		weights matrix,
		used for the linear transformation of the recurrent state..
	- __bias_initializer__: Initializer for the bias vector.

	- __unit_forget_bias__: Boolean.

		If True, add 1 to the bias of the forget gate at initialization.
		Setting it to true will also force `bias_initializer="zeros"`.
		This is recommended in [Jozefowicz et
		  al.](http://www.jmlr.org/proceedings/papers/v37/jozefowicz15.pdf)
	- __kernel_regularizer__: Regularizer function applied to

		the `kernel` weights matrix.
	- __recurrent_regularizer__: Regularizer function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_regularizer__: Regularizer function applied to the bias vector.

	- __activity_regularizer__: Regularizer function applied to

		the output of the layer (its "activation")..
	- __kernel_constraint__: Constraint function applied to

		the `kernel` weights matrix.
	- __recurrent_constraint__: Constraint function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.

	- __dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the inputs.
	- __recurrent_dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the recurrent state.

- __References__:

	- [Long short-term
	  memory]((http://www.bioinf.jku.at/publications/older/2604.pdf)
	  (original 1997 paper)
	- [Supervised sequence labeling with recurrent neural
	  networks](http://www.cs.toronto.edu/~graves/preprint.pdf)
	- [A Theoretically Grounded Application of Dropout in Recurrent Neural
	  Networks](http://arxiv.org/abs/1512.05287)

Polyaxonfile usage:

```yaml
LSTM:
  units: 3
  activation: tanh
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/recurrent.py#L329)</span>
## GRUConfig

```python
polyaxon_schemas.layers.recurrent.GRUConfig(units, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer=<polyaxon_schemas.initializations.GlorotUniformInitializerConfig object at 0x10774ef98>, recurrent_initializer=<polyaxon_schemas.initializations.OrthogonalInitializerConfig object at 0x10774ef60>, bias_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x10774efd0>, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Gated Recurrent Unit - Cho et al.

2014.

- __Args__:

	- __units__: Positive integer, dimensionality of the output space.

	- __activation__: Activation function to use.

		If you pass None, no activation is applied
		(ie. "linear" activation: `a(x) = x`).
	- __recurrent_activation__: Activation function to use

		for the recurrent step.
	- __use_bias__: Boolean, whether the layer uses a bias vector.

	- __kernel_initializer__: Initializer for the `kernel` weights matrix,

		used for the linear transformation of the inputs..
	- __recurrent_initializer__: Initializer for the `recurrent_kernel`

		weights matrix,
		used for the linear transformation of the recurrent state..
	- __bias_initializer__: Initializer for the bias vector.

	- __kernel_regularizer__: Regularizer function applied to

		the `kernel` weights matrix.
	- __recurrent_regularizer__: Regularizer function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_regularizer__: Regularizer function applied to the bias vector.

	- __activity_regularizer__: Regularizer function applied to

		the output of the layer (its "activation")..
	- __kernel_constraint__: Constraint function applied to

		the `kernel` weights matrix.
	- __recurrent_constraint__: Constraint function applied to

		the `recurrent_kernel` weights matrix.
	- __bias_constraint__: Constraint function applied to the bias vector.

	- __dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the inputs.
	- __recurrent_dropout__: Float between 0 and 1.

		Fraction of the units to drop for
		the linear transformation of the recurrent state.

- __References__:

	- [On the Properties of Neural Machine Translation: Encoder-Decoder
	  Approaches](https://arxiv.org/abs/1409.1259)
	- [Empirical Evaluation of Gated Recurrent Neural Networks on Sequence
	  Modeling](http://arxiv.org/abs/1412.3555v1)
	- [A Theoretically Grounded Application of Dropout in Recurrent Neural
	  Networks](http://arxiv.org/abs/1512.05287)

Polyaxonfile usage:

```yaml
GRU:
  units: 3
  activation: tanh
```
