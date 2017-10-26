<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon-docs/blob/master/polyaxon/layers/recurrent.py#L19)</span>
## Recurrent

```python
polyaxon.layers.recurrent.Recurrent(return_sequences=False, return_state=False, go_backwards=False, stateful=False, unroll=False, implementation=0)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon-docs/blob/master/polyaxon/layers/recurrent.py#L23)</span>
## SimpleRNN

```python
polyaxon.layers.recurrent.SimpleRNN(units, activation='tanh', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Fully-connected RNN where the output is to be fed back to input.

- __Arguments__:
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon-docs/blob/master/polyaxon/layers/recurrent.py#L105)</span>
## LSTM

```python
polyaxon.layers.recurrent.LSTM(units, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', unit_forget_bias=True, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Long-Short Term Memory unit - Hochreiter 1997.

  For a step-by-step description of the algorithm, see
  [this tutorial](http://deeplearning.net/tutorial/lstm.html).

- __Arguments__:
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon-docs/blob/master/polyaxon/layers/recurrent.py#L63)</span>
## GRU

```python
polyaxon.layers.recurrent.GRU(units, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0)
```

Gated Recurrent Unit - Cho et al.

  2014.

- __Arguments__:
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
  