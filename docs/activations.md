## linear


```python
linear(name='Linear', collect=True)
```


Computes linear/identity function.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## built_activation


```python
built_activation(x, collect)
```


Builds the metric function.

- __Args__:
	- __x__: activated tensor.
	- __collect__: whether to collect this metric under the metric collection.


----

## tanh


```python
tanh(name=None, collect=True)
```


Computes hyperbolic tangent of x element-wise.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## hard_sigmoid


```python
hard_sigmoid(name='HardSigmoid', collect=True)
```


Segment-wise linear approximation of sigmoid.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## sigmoid


```python
sigmoid(name=None, collect=True)
```


Computes sigmoid of `x` element-wise: `y = 1 / (1 + exp(-x))`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## softmax


```python
softmax(name=None, collect=True)
```


Computes softmax activations.

For each batch `i` and class `j` we have
	`softmax[i, j] = exp(logits[i, j]) / sum(exp(logits[i]))`

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## softplus


```python
softplus(name=None, collect=True)
```


Computes softplus. `log(exp(features) + 1)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## softsign


```python
softsign(name=None, collect=True)
```


Computes softsign: `features / (abs(features) + 1)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## relu


```python
relu(name=None, collect=True)
```


Computes ReLU, rectified linear: `max(features, 0)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## relu6


```python
relu6(name=None, collect=True)
```


Computes Rectified Linear 6: `min(max(features, 0), 6)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## elu


```python
elu(name=None, collect=True)
```


Computes Exponential Linear Unit.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## selu


```python
selu(name='Selu', collect=True)
```


Scaled Exponential Linear Unit. (Klambauer et al., 2017).

- __Arguments__:
	- __x__: A tensor or variable to compute the activation function for.

- __Returns__:
  Tensor with the same shape and dtype as `x`.

- __References__:
	- [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)


----

## crelu


```python
crelu(name=None, collect=True)
```


Computes Concatenated ReLU.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.
