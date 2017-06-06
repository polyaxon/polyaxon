<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L116)</span>
### SimpleRNN

```python
polyaxon.layers.recurrent.SimpleRNN(mode, num_units, activation='sigmoid', dropout=None, num_layers=1, bias=True, weights_init=None, return_seq=False, return_state=False, initial_state=None, dynamic=False, trainable=True, restore=True, name='SimpleRNN')
```

Simple RNN (Simple Recurrent Layer.)

- __Output__:
if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
- __else__: 2-D Tensor [samples, output dim].

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'sigmoid'.
- __dropout__: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
	input and output keep probability.
- __num_layers__: `int` how many times to stack the cell.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __return_seq__: `bool`. If True, returns the full sequence instead of
	last sequence output only.
- __return_state__: `bool`. If True, returns a tuple with output and
	- __states__: (output, states).
- __initial_state__: `Tensor`. An initial state for the RNN.  This must be
	a tensor of appropriate type and shape [batch_size x cell.state_size].
- __dynamic__: `bool`. If True, dynamic computation is performed. It will not
	compute RNN steps above the sequence length. Note that because TF
	requires to feed sequences of same length, 0 is used as a mask.
	So a sequence padded with 0 at the end must be provided. When
	computation is performed, it will stop when it meets a step with
	a value of 0.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L177)</span>
### LSTM

```python
polyaxon.layers.recurrent.LSTM(mode, num_units, activation='tanh', inner_activation='sigmoid', dropout=None, num_layers=1, bias=True, weights_init=None, forget_bias=1.0, return_seq=False, return_state=False, initial_state=None, dynamic=False, trainable=True, restore=True, name='LSTM')
```

LSTM (Long Short Term Memory Recurrent Layer).

- __Output__:
if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
- __else__: 2-D Tensor [samples, output dim].

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
- __inner_activation__: `str` (name) or `function` (returning a `Tensor`).
	LSTM inner activation. Default: 'sigmoid'.
- __dropout__: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
	input and output keep probability.
- __num_layers__: `int` how many times to stack the cell.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __forget_bias__: `float`. Bias of the forget gate. Default: 1.0.
- __return_seq__: `bool`. If True, returns the full sequence instead of
	last sequence output only.
- __return_state__: `bool`. If True, returns a tuple with output and
	- __states__: (output, states).
- __initial_state__: `Tensor`. An initial state for the RNN.  This must be
	a tensor of appropriate type and shape [batch_size x cell.state_size].
- __dynamic__: `bool`. If True, dynamic computation is performed. It will not
	compute RNN steps above the sequence length. Note that because TF
	requires to feed sequences of same length, 0 is used as a mask.
	So a sequence padded with 0 at the end must be provided. When
	computation is performed, it will stop when it meets a step with
	a value of 0.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

- __References__:
Long Short Term Memory, Sepp Hochreiter & Jurgen Schmidhuber,
Neural Computation 9(8): 1735-1780, 1997.

- __Links__:
- __[http__://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf]
(http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L253)</span>
### GRU

```python
polyaxon.layers.recurrent.GRU(mode, num_units, activation='tanh', inner_activation='sigmoid', dropout=None, num_layers=1, bias=True, weights_init=None, return_seq=False, return_state=False, initial_state=None, dynamic=False, trainable=True, restore=True, name='GRU')
```

GRU (Gated Recurrent Unit Layer).

- __Output__:
if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
- __else__: 2-D Tensor [samples, output dim].

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
- __inner_activation__: `str` (name) or `function` (returning a `Tensor`).
	GRU inner activation. Default: 'sigmoid'.
- __dropout__: `tuple` of `float`: (1 - input_keep_prob, 1 - output_keep_prob). The
	input and output keep probability.
- __num_layers__: `int` how many times to stack the cell.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __return_seq__: `bool`. If True, returns the full sequence instead of
	last sequence output only.
- __return_state__: `bool`. If True, returns a tuple with output and
	- __states__: (output, states).
- __initial_state__: `Tensor`. An initial state for the RNN.  This must be
	a tensor of appropriate type and shape [batch_size x cell.state_size].
- __dynamic__: `bool`. If True, dynamic computation is performed. It will not
	compute RNN steps above the sequence length. Note that because TF
	requires to feed sequences of same length, 0 is used as a mask.
	So a sequence padded with 0 at the end must be provided. When
	computation is performed, it will stop when it meets a step with
	a value of 0.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

- __References__:
Learning Phrase Representations using RNN Encoder–Decoder for
Statistical Machine Translation, K. Cho et al., 2014.

- __Links__:
- __[http__://arxiv.org/abs/1406.1078](http://arxiv.org/abs/1406.1078)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L325)</span>
### BidirectionalRNN

```python
polyaxon.layers.recurrent.BidirectionalRNN(mode, rnncell_fw, rnncell_bw, return_seq=False, return_states=False, initial_state_fw=None, initial_state_bw=None, dynamic=False, name='BiRNN')
```

Bidirectional RNN.

Build a bidirectional recurrent neural network, it requires 2 RNN Cells
to process sequence in forward and backward order. Any RNN Cell can be
used i.e. SimpleRNN, LSTM, GRU... with its own parameters. But the two
cells number of units must match.

- __Output__:
if `return_seq`: 3-D Tensor [samples, timesteps, output dim].
- __else__: 2-D Tensor Layer [samples, output dim].

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __rnncell_fw__: `RNNCell`. The RNN Cell to use for foward computation.
- __rnncell_bw__: `RNNCell`. The RNN Cell to use for backward computation.
- __return_seq__: `bool`. If True, returns the full sequence instead of
	last sequence output only.
- __return_states__: `bool`. If True, returns a tuple with output and
	- __states__: (output, states).
- __initial_state_fw__: `Tensor`. An initial state for the forward RNN.
	This must be a tensor of appropriate type and shape [batch_size
	x cell.state_size].
- __initial_state_bw__: `Tensor`. An initial state for the backward RNN.
	This must be a tensor of appropriate type and shape [batch_size
	x cell.state_size].
- __dynamic__: `bool`. If True, dynamic computation is performed. It will not
	compute RNN steps above the sequence length. Note that because TF
	requires to feed sequences of same length, 0 is used as a mask.
	So a sequence padded with 0 at the end must be provided. When
	computation is performed, it will stop when it meets a step with
	a value of 0.
- __name__: `str`. A name for this layer (optional).


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L446)</span>
### BasicRNNCell

```python
polyaxon.layers.recurrent.BasicRNNCell(mode, num_units, activation='tanh', bias=True, weights_init=None, trainable=True, restore=True, name='BasicRNNCell')
```

The most basic RNN cell with custom params.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L492)</span>
### GRUCell

```python
polyaxon.layers.recurrent.GRUCell(mode, num_units, activation='tanh', inner_activation='sigmoid', bias=True, weights_init=None, trainable=True, restore=True, name='GRUCell')
```

Gated Recurrent Unit cell with custom params.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
- __inner_activation__: `str` (name) or `function` (returning a `Tensor`).
	GRU inner activation. Default: 'sigmoid'.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L557)</span>
### BasicLSTMCell

```python
polyaxon.layers.recurrent.BasicLSTMCell(mode, num_units, forget_bias=1.0, state_is_tuple=True, activation='tanh', inner_activation='sigmoid', bias=True, weights_init=None, batch_norm=False, trainable=True, restore=True, name='BasicLSTMCell')
```

Basic LSTM recurrent network cell with custo\m params.

The implementation is based on: http://arxiv.org/abs/1409.2329.

We add forget_bias (default: 1) to the biases of the forget gate in order to
reduce the scale of forgetting in the beginning of the training.

It does not allow cell clipping, a projection layer, and does not
use peep-hole connections: it is the basic baseline.

For advanced models, please use the full LSTMCell that follows.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __num_units__: `int`, number of units for this layer.
- __forget_bias__: `float`. Bias of the forget gate. Default: 1.0.
- __state_is_tuple__: If True, accepted and returned states are n-tuples, where
	`n = len(cells)`.  If False, the states are all
	concatenated along the column axis.  This latter behavior will soon be
	deprecated.
- __activation__: `str` (name) or `function` (returning a `Tensor`). Default: 'tanh'.
- __inner_activation__: `str` (name) or `function` (returning a `Tensor`).
	GRU inner activation. Default: 'sigmoid'.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
- __batch_norm__: `bool`. If True, use batch normalization for this cell.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when loading a model.
- __name__: `str`. A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L677)</span>
### DropoutWrapper

```python
polyaxon.layers.recurrent.DropoutWrapper(mode, cell, input_keep_prob=1.0, output_keep_prob=1.0, seed=None, name='DropoutWrapper')
```

Operator adding dropout to inputs and outputs of the given cell.

Creates a cell with added input and/or output dropout.

Dropout is never used on the state.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __cell__: an RNNCell, a projection to output_size is added to it.
- __input_keep_prob__: unit Tensor or float between 0 and 1, input keep probability;
	if it is float and 1, no input dropout will be added.
- __output_keep_prob__: unit Tensor or float between 0 and 1, output keep
probability; if it is float and 1, no output dropout will be added.
- __seed__: (optional) integer, the randomness seed.

- __Raises__:
  - __TypeError__: if cell is not an RNNCell.
  - __ValueError__: if keep_prob is not between 0 and 1.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/recurrent.py#L749)</span>
### MultiRNNCell

```python
polyaxon.layers.recurrent.MultiRNNCell(mode, cells, state_is_tuple=True, name='MultiRNNCell')
```

RNN cell composed sequentially of multiple simple cells.

Create a RNN cell composed sequentially of a number of RNNCells.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __cells__: list of RNNCells that will be composed in this order.
- __state_is_tuple__: If True, accepted and returned states are n-tuples, where
	`n = len(cells)`.  If False, the states are all
	concatenated along the column axis.  This latter behavior will soon be
	deprecated.

- __Raises__:
- __ValueError__: if cells is empty (not allowed), or at least one of the cells
	returns a state tuple but the flag `state_is_tuple` is `False`.
