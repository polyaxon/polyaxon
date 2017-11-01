<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L55)</span>

## absolute_difference


```python
absolute_difference(weights=1.0, name='AbsoluteDifference', scope=None, collect=True)
```


Adds an Absolute Difference loss to the training procedure.

`weights` acts as a coefficient for the loss. If a scalar is provided, then
the loss is simply scaled by the given value. If `weights` is a `Tensor` of
shape `[batch_size]`, then the total loss for each sample of the batch is
rescaled by the corresponding element in the `weights` vector. If the shape of
`weights` matches the shape of `predictions`, then the loss of each
measurable element of `predictions` is scaled by the corresponding value of
`weights`.

- __Args__:

	- __weights__: Optional `Tensor` whose rank is either 0, or the same rank as

	`labels`, and must be broadcastable to `labels` (i.e., all dimensions must
	be either `1`, or the same as the corresponding `losses` dimension).
	- __name__: operation name.

	- __scope__: operation scope.

	- __collect__: whether to collect this metric under the metric collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L84)</span>

## log_loss


```python
log_loss(weights=1.0, epsilon=1e-07, name='LogLoss', scope=None, collect=True)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L95)</span>

## mean_squared_error


```python
mean_squared_error(weights=1.0, name='MeanSquaredError', scope=None, collect=True)
```


Computes Mean Square Loss.

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __scope__: scope to add the op to.

	- __name__: name of the op.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L117)</span>

## huber_loss


```python
huber_loss(weights=1.0, clip=0.0, name='HuberLoss', scope=None, collect=True)
```


Computes Huber Loss for DQN.

[Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
[DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __scope__: scope to add the op to.

	- __name__: name of the op.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L146)</span>

## clipped_delta_loss


```python
clipped_delta_loss(weights=1.0, clip_value_min=-1.0, clip_value_max=1.0, name='HuberLoss', scope=None, collect=True)
```


Computes clipped delta Loss for DQN.

[Wikipedia link](https://en.wikipedia.org/wiki/Huber_loss)
[DeepMind link](https://sites.google.com/a/deepmind.com/dqn/)

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __scope__: scope to add the op to.

	- __name__: name of the op.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L176)</span>

## softmax_cross_entropy


```python
softmax_cross_entropy(weights=1.0, label_smoothing=0, name='SoftmaxCrossEntropy', scope=None, collect=True)
```


Computes Softmax Cross entropy (softmax categorical cross entropy).

Computes softmax cross entropy between y_pred (logits) and
y_true (labels).

Measures the probability error in discrete classification tasks in which
the classes are mutually exclusive (each entry is in exactly one class).
For example, each CIFAR-10 image is labeled with one and only one label:
an image can be a dog or a truck, but not both.

- __**WARNING__:** This op expects unscaled logits, since it performs a `softmax`

on `y_pred` internally for efficiency.  Do not call this op with the
output of `softmax`, as it will produce incorrect results.

`y_pred` and `y_true` must have the same shape `[batch_size, num_classes]`
and the same dtype (either `float32` or `float64`). It is also required
that `y_true` (labels) are binary arrays (For example, class 2 out of a
total of 5 different classes, will be define as [0., 1., 0., 0., 0.])

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __label_smoothing__: If greater than `0` then smooth the labels.

	- __scope__: scope to add the op to.

	- __name__: name of the op.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L226)</span>

## sigmoid_cross_entropy


```python
sigmoid_cross_entropy(weights=1.0, label_smoothing=0, name='SigmoidCrossEntropy', scope=None, collect=True)
```


Computes Sigmoid cross entropy.(binary cross entropy):

Computes sigmoid cross entropy between y_pred (logits) and y_true
(labels).

Measures the probability error in discrete classification tasks in which
each class is independent and not mutually exclusive. For instance,
one could perform multilabel classification where a picture can contain
both an elephant and a dog at the same time.

For brevity, let `x = logits`, `z = targets`.  The logistic loss is

  x - x * z + log(1 + exp(-x))

To ensure stability and avoid overflow, the implementation uses

  max(x, 0) - x * z + log(1 + exp(-abs(x)))

`y_pred` and `y_true` must have the same type and shape.

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __label_smoothing__: If greater than `0` then smooth the labels.

	- __scope__: scope to add the op to.

	- __name__: name of the op.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L274)</span>

## hinge_loss


```python
hinge_loss(weights=1.0, name='HingeLoss', scope=None, collect=True)
```


Hinge Loss.

- __Args__:

	- __weights__: Coefficients for the loss a `scalar`.

	- __name__: name of the op.

	- __scope__: The scope for the operations performed in computing the loss.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L299)</span>

## cosine_distance


```python
cosine_distance(dim, weights=1.0, name='CosineDistance', scope=None, collect=True)
```


Adds a cosine-distance loss to the training procedure.

Note that the function assumes that `predictions` and `labels` are already unit-normalized.

- __WARNING__: `weights` also supports dimensions of 1, but the broadcasting does

not work as advertised, you'll wind up with weighted sum instead of weighted
mean for any but the last dimension. This will be cleaned up soon, so please
do not rely on the current behavior for anything but the shapes documented for
`weights` below.

- __Args__:

	- __dim__: The dimension along which the cosine distance is computed.

	- __weights__: Coefficients for the loss a `scalar`.

	- __name__: name of the op.

	- __scope__: The scope for the operations performed in computing the loss.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L332)</span>

## kullback_leibler_divergence


```python
kullback_leibler_divergence(weights=1.0, name='KullbackLeiberDivergence', scope=None, collect=False)
```


Adds a Kullback leiber diverenge loss to the training procedure.

 - __Args__:

	- __name__: name of the op.

	- __scope__: The scope for the operations performed in computing the loss.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/losses.py#L357)</span>

## poisson_loss


```python
poisson_loss(weights=1.0, name='PoissonLoss', scope=None, collect=False)
```


Adds a poisson loss to the training procedure.

 - __Args__:

	- __name__: name of the op.

	- __scope__: The scope for the operations performed in computing the loss.

	- __collect__: add to losses collection.


- __Returns__:

	A scalar `Tensor` representing the loss value.

- __Raises__:

	- __ValueError__: If `predictions` shape doesn't match `labels` shape, or `weights` is `None`.

