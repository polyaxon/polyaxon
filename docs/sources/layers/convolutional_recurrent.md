<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional_recurrent.py#L14)</span>
## ConvRecurrent2D

```python
polyaxon.layers.convolutional_recurrent.ConvRecurrent2D(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), return_sequences=False, go_backwards=False, stateful=False)
```

Abstract base class for convolutional recurrent layers.

  Do not use in a model -- it's not a functional layer!

- __Arguments__:
	- __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
	- __kernel_size__: An integer or tuple/list of n integers, specifying the
	  dimensions of the convolution window.
	- __strides__: An integer or tuple/list of n integers,
	  specifying the strides of the convolution.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).
	- __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, time, ..., channels)`
	  while `channels_first` corresponds to
	  inputs with shape `(batch, time, channels, ...)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
	  If you never set it, then it will be "channels_last".
	- __dilation_rate__: An integer or tuple/list of n integers, specifying
	  the dilation rate to use for dilated convolution.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any `strides` value != 1.
	- __return_sequences__: Boolean. Whether to return the last output
	  in the output sequence, or the full sequence.
	- __go_backwards__: Boolean (default False).
	  If True, rocess the input sequence backwards.
	- __stateful__: Boolean (default False). If True, the last state
	  for each sample at index i in a batch will be used as initial
	  state for the sample of index i in the following batch.

  Input shape:
  5D tensor with shape `(num_samples, timesteps, channels, rows, cols)`.

  Output shape:
  - if `return_sequences`: 5D tensor with shape
	  `(num_samples, timesteps, channels, rows, cols)`.
  - else, 4D tensor with shape `(num_samples, channels, rows, cols)`.

  # Masking
  This layer supports masking for input data with a variable number
  of timesteps. To introduce masks to your data,
  use an `Embedding` layer with the `mask_zero` parameter
  set to `True`.
	- __**Note__:** for the time being, masking is only supported with Theano.

  # Note on using statefulness in RNNs
  You can set RNN layers to be 'stateful', which means that the states
  computed for the samples in one batch will be reused as initial states
  for the samples in the next batch.
  This assumes a one-to-one mapping between
  samples in different successive batches.

  To enable statefulness:
	  - specify `stateful=True` in the layer constructor.
	  - specify a fixed batch size for your model, by passing
		  a `batch_input_size=(...)` to the first layer in your model.
		  This is the expected shape of your inputs *including the batch
		  size*.
		  It should be a tuple of integers, e.g. `(32, 10, 100)`.

  To reset the states of your model, call `.reset_states()` on either
  a specific layer, or on your entire model.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/convolutional_recurrent.py#L19)</span>
## ConvLSTM2D

```python
polyaxon.layers.convolutional_recurrent.ConvLSTM2D(filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', unit_forget_bias=True, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, return_sequences=False, go_backwards=False, stateful=False, dropout=0.0, recurrent_dropout=0.0)
```

Convolutional LSTM.

  It is similar to an LSTM layer, but the input transformations
  and recurrent transformations are both convolutional.

- __Arguments__:
	- __filters__: Integer, the dimensionality of the output space
	  (i.e. the number output of filters in the convolution).
	- __kernel_size__: An integer or tuple/list of n integers, specifying the
	  dimensions of the convolution window.
	- __strides__: An integer or tuple/list of n integers,
	  specifying the strides of the convolution.
	  Specifying any stride value != 1 is incompatible with specifying
	  any `dilation_rate` value != 1.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).
	- __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, time, ..., channels)`
	  while `channels_first` corresponds to
	  inputs with shape `(batch, time, channels, ...)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
	  If you never set it, then it will be "channels_last".
	- __dilation_rate__: An integer or tuple/list of n integers, specifying
	  the dilation rate to use for dilated convolution.
	  Currently, specifying any `dilation_rate` value != 1 is
	  incompatible with specifying any `strides` value != 1.
	- __activation__: Activation function to use.
	  If you don't specify anything, no activation is applied
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
	  Use in combination with `bias_initializer="zeros"`.
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
	- __return_sequences__: Boolean. Whether to return the last output
	  in the output sequence, or the full sequence.
	- __go_backwards__: Boolean (default False).
	  If True, rocess the input sequence backwards.
	- __stateful__: Boolean (default False). If True, the last state
	  for each sample at index i in a batch will be used as initial
	  state for the sample of index i in the following batch.
	- __dropout__: Float between 0 and 1.
	  Fraction of the units to drop for
	  the linear transformation of the inputs.
	- __recurrent_dropout__: Float between 0 and 1.
	  Fraction of the units to drop for
	  the linear transformation of the recurrent state.

  Input shape:
  - if data_format='channels_first'
	  5D tensor with shape:
	  `(samples,time, channels, rows, cols)`
  - if data_format='channels_last'
	  5D tensor with shape:
	  `(samples,time, rows, cols, channels)`

   Output shape:
  - if `return_sequences`
	   - if data_format='channels_first'
		  5D tensor with shape:
		  `(samples, time, filters, output_row, output_col)`
	   - if data_format='channels_last'
		  5D tensor with shape:
		  `(samples, time, output_row, output_col, filters)`
  - else
	  - if data_format ='channels_first'
		  4D tensor with shape:
		  `(samples, filters, output_row, output_col)`
	  - if data_format='channels_last'
		  4D tensor with shape:
		  `(samples, output_row, output_col, filters)`
	  where o_row and o_col depend on the shape of the filter and
	  the padding

- __Raises__:
	- __ValueError__: in case of invalid constructor arguments.

- __References__:
  - [Convolutional LSTM Network: A Machine Learning Approach for
  Precipitation Nowcasting](http://arxiv.org/abs/1506.04214v1)
  The current implementation does not include the feedback loop on the
  cells output
  