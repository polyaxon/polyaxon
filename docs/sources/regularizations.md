### built_regularizer


```python
built_regularizer(fct, collect)
```


Builds the regularizer function.

- __Args__:
- __fct__: the metric function to build.
- __collect__: whether to collect this metric under the metric collection.

----

### l2_regularizer


```python
l2_regularizer(scale=0.001, name='l2Regularizer', collect=True)
```


Returns a function that can be used to apply L2 regularization to a tensor.

Computes half the L2 norm of a tensor without the `sqrt`:

  output = sum(t ** 2) / 2 * wd

- __Args__:
- __x__: `Tensor`. The tensor to apply regularization.
- __scale__: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
- __name__: `str` name of the app.
- __collect__: add to regularization losses

- __Returns__:
The regularization `Tensor`.

----

### l1_regularizer


```python
l1_regularizer(scale=0.001, name='l1Regularizer', collect=True)
```


Returns a function that can be used to apply L1 regularization to a tensor.

Computes the L1 norm of a tensor:

  output = sum(|t|) * scale

- __Args__:
- __scale__: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
- __name__: name of the app.
- __collect__: add to regularization losses

- __Returns__:
The regularization `Tensor`.

----

### l2_l1_regularizer


```python
l2_l1_regularizer(scale_l1=0.001, scale_l2=0.001, name='l2l1Regularizer', collect=True)
```


Returns a function that can be used to apply L2 L1 regularization to a tensor.

Computes the L2 and L1 norm of a tensor:

- __Args__:
- __scale_l1__: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
- __scale_l2__: `float`. A scalar multiplier `Tensor`. 0.0 disables the regularizer.
- __name__: name of the app.
- __collect__: add to regularization losses

- __Returns__:
The regularization `Tensor`.
