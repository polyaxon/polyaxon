## built_activation


```python
built_activation(fct, name, collect)
```


Builds the metric function.

- __Args__:
	- __fct__: the activation function to build.
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## linear


```python
linear(name='Linear', collect=False)
```


Computes linear/identity function.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## tanh


```python
tanh(name=None, collect=False)
```


Computes hyperbolic tangent of x element-wise.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## sigmoid


```python
sigmoid(name=None, collect=False)
```


Computes sigmoid of `x` element-wise: `y = 1 / (1 + exp(-x))`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## softmax


```python
softmax(name=None, collect=False)
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
softplus(name=None, collect=False)
```


Computes softplus. `log(exp(features) + 1)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## softsign


```python
softsign(name=None, collect=False)
```


Computes softsign: `features / (abs(features) + 1)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## relu


```python
relu(name=None, collect=False)
```


Computes ReLU, rectified linear: `max(features, 0)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## relu6


```python
relu6(name=None, collect=False)
```


Computes Rectified Linear 6: `min(max(features, 0), 6)`.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## leaky_relu


```python
leaky_relu(alpha=0.1, name='LeakyReLU', collect=False)
```


Modified version of ReLU, introducing a nonzero gradient for negative input.

- __Args__:
	- __alpha__: `int`, the multiplier.
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## prelu


```python
prelu(channel_shared=False, weights_init='zeros', restore=True, name='PReLU', collect=False)
```


Parametric Rectified Linear Unit.

- __Args__:
	- __channel_shared__:
	- __weights_init__:
	- __restore__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## elu


```python
elu(name=None, collect=False)
```


Computes Exponential Linear Unit.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.


----

## crelu


```python
crelu(name='CRelu', collect=False)
```


Computes Concatenated ReLU.

- __Args__:
	- __name__: operation name.
	- __collect__: whether to collect this metric under the metric collection.
