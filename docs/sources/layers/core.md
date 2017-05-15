<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L16)</span>
### FullyConnected

```python
polyaxon.layers.core.FullyConnected(mode, n_units, activation='linear', bias=True, weights_init='truncated_normal', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='FullyConnected')
```

Adds a fully connected layer.

`fully_connected` creates a variable called `w`, representing a fully
connected weight matrix, which is multiplied by the `incoming` to produce a
`Tensor` of hidden units.

- __Note__: that if `inputs` have a rank greater than 2, then `inputs` is flattened
prior to the initial matrix multiply by `weights`.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __n_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`).
	- __Default__: 'linear'.
- __bias__: `bool`. If True, a bias is used.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
	- __Default__: 'truncated_normal'.
- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
	- __Default__: 'zeros'.
- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
	- __Default__: None.
- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when
	loading a model.
- __name__: A name for this layer (optional). Default: 'FullyConnected'.

- __Attributes__:
- __w__: `Tensor`. Variable representing units weights.
- __b__: `Tensor`. Variable representing biases.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L111)</span>
### Dropout

```python
polyaxon.layers.core.Dropout(mode, keep_prob, noise_shape=None, seed=None, name='Dropout')
```

Adds a Dropout op to the input.

Outputs the input element scaled up by `1 / keep_prob`. The scaling is so
that the expected sum is unchanged.

By default, each element is kept or dropped independently. If noise_shape
is specified, it must be broadcastable to the shape of x, and only dimensions
with noise_shape[i] == shape(x)[i] will make independent decisions. For
example, if shape(x) = [k, l, m, n] and noise_shape = [k, 1, 1, n], each
batch and channel component will be kept independently and each row and column
will be kept or not kept together.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
keep_prob : A float representing the probability that each element
	is kept.
noise_shape : A 1-D Tensor of type int32, representing the shape for
	randomly generated keep/drop flags.
name : A name for this layer (optional).

- __References__:
- __Dropout__: A Simple Way to Prevent Neural Networks from Overfitting.
N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever & R. Salakhutdinov,
(2014), Journal of Machine Learning Research, 5(Jun)(2), 1929-1958.

- __Links__:
  - __[https__://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf]
(https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf)

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L174)</span>
### Reshape

```python
polyaxon.layers.core.Reshape(mode, new_shape, name='Reshape')
```

Reshape.

A layer that reshape the incoming layer tensor output to the desired shape.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __new_shape__: A list of `int`. The desired shape.
- __name__: A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L202)</span>
### Flatten

```python
polyaxon.layers.core.Flatten(mode, name='Flatten')
```

Flatten the incoming Tensor.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L228)</span>
### SingleUnit

```python
polyaxon.layers.core.SingleUnit(mode, activation='linear', bias=True, trainable=True, restore=True, name='Linear')
```

Adds a Single Unit Layer.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __activation__: `str` (name) or `function`. Activation applied to this layer. Default: 'linear'.
- __bias__: `bool`. If True, a bias is used.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when
	loading a model.
- __name__: A name for this layer (optional). Default: 'Linear'.

- __Attributes__:
- __W__: `Tensor`. Variable representing weight.
- __b__: `Tensor`. Variable representing bias.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L296)</span>
### Highway

```python
polyaxon.layers.core.Highway(mode, n_units, activation='linear', transform_dropout=None, weights_init='truncated_normal', bias_init='zeros', regularizer=None, scale=0.001, trainable=True, restore=True, name='FullyConnectedHighway')
```

Adds Fully Connected Highway.

A fully connected highway network layer, with some inspiration from
- __[https__://github.com/fomorians/highway-fcn](https://github.com/fomorians/highway-fcn).

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __n_units__: `int`, number of units for this layer.
- __activation__: `str` (name) or `function` (returning a `Tensor`).
	- __Default__: 'linear'.
- __transform_dropout__: `float`: Keep probability on the highway transform gate.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
	- __Default__: 'truncated_normal'.
- __bias_init__: `str` (name) or `Tensor`. Bias initialization.
	- __Default__: 'zeros'.
- __regularizer__: `str` (name) or `Tensor`. Add a regularizer to this layer weights.
	- __Default__: None.
- __scale__: `float`. Regularizer decay parameter. Default: 0.001.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when
	loading a model.
- __name__: A name for this layer (optional). Default: 'FullyConnectedHighway'.

- __Attributes__:
- __W__: `Tensor`. Variable representing units weights.
- __W_t__: `Tensor`. Variable representing units weights for transform gate.
- __b__: `Tensor`. Variable representing biases.
- __b_t__: `Tensor`. Variable representing biases for transform gate.

- __Links__:
- __[https__://arxiv.org/abs/1505.00387](https://arxiv.org/abs/1505.00387)

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L417)</span>
### OneHotEncoding

```python
polyaxon.layers.core.OneHotEncoding(mode, n_classes, on_value=1.0, off_value=0.0, name='OneHotEncoding')
```

Transform numeric labels into one hot labels using `tf.one_hot`.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __n_classes__: `int`. Total number of classes.
- __on_value__: `scalar`. A scalar defining the on-value.
- __off_value__: `scalar`. A scalar defining the off-value.
- __name__: A name for this layer (optional). Default: 'OneHotEncoding'.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L449)</span>
### Merge

```python
polyaxon.layers.core.Merge(mode, merge_mode, axis=1, name='Merge')
```

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L523)</span>
### Concat

```python
polyaxon.layers.core.Concat(mode, name='Concat')
```

Concat Outputs.

A layer that concatenate all outputs of a network into a single tensor.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`. A name for this layer (optional).

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/core.py#L547)</span>
### Slice

```python
polyaxon.layers.core.Slice(mode, begin, size, name='Slice')
```

Extracts a slice from a tensor.

This operation extracts a slice of size size from a tensor input starting at
the location specified by begin.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`. A name for this layer (optional).
