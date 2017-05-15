### top_k


```python
top_k(k=1, name='TopK', scope=None, collect=False)
```


top_k_op.

An op that calculates top-k mean accuracy.

- __Examples__:
```python
>>> input_data = placeholder(shape=[None, 784])
>>> y_pred = my_network(input_data) # Apply some ops
>>> y_true = placeholder(shape=[None, 10]) # Labels
>>> top3_op = top_k(y_pred, y_true, 3)

>>> # Calculate Top-3 accuracy by feeding data X and labels Y
>>> top3_accuracy = sess.run(top3_op, feed_dict={input_data: X, y_true: Y})
```

- __Args__:
- __k__: `int`. Number of top elements to look at for computing precision.
- __scope__: scope to add the op to.
- __name__: name of the op.
- __collect__: add to metrics collection.

- __Returns__:
`Float`. The top-k mean accuracy.

----

### std_error


```python
std_error(name='StandardError', scope=None, collect=False)
```


standard error.

An op that calculates the standard error.

- __Examples__:
```python
>>> input_data = placeholder(shape=[None, 784])
>>> y_pred = my_network(input_data) # Apply some ops
>>> y_true = placeholder(shape=[None, 10]) # Labels
>>> stderr = std_error(y_pred, y_true)

>>> # Calculate standard error by feeding data X and labels Y
>>> std_error = sess.run(stderr_op, feed_dict={input_data: X, y_true: Y})
```

- __Args__:
- __scope__: scope to add the op to.
- __name__: name of the op.
- __collect__: add to metrics collection.

- __Returns__:
`Float`. The standard error.

----

### accuracy


```python
accuracy(name='Accuracy', scope=None, collect=False)
```


Computes the accuracy.

An op that calculates mean accuracy:
* y_pred are y_True are both one-hot encoded. (categorical accuracy)
* y_pred are logits are binary encoded (and represented as int32). (binary accuracy)


- __Examples__:
```python
>>> input_data = placeholder(shape=[None, 784])
>>> y_pred = my_network(input_data) # Apply some ops
>>> y_true = placeholder(shape=[None, 10]) # Labels
>>> accuracy_op = accuracy(y_pred, y_true)
>>> # Calculate accuracy by feeding data X and labels Y
>>> accuracy_op = sess.run(accuracy_op, feed_dict={input_data: X, y_true: Y})
```

- __Args__:
- __scope__: scope to add the op to.
- __name__: name of the op.
- __collect__: add to metrics collection.

- __Returns__:
`Float`. The mean accuracy.

----

### check_metric_data


```python
check_metric_data(y_pred, y_true)
```

----

### built_metric


```python
built_metric(fct, name, scope, collect)
```


Builds the metric function.

- __Args__:
- __fct__: the metric function to build.
- __name__: operation name.
- __scope__: operation scope.
- __collect__: whether to collect this metric under the metric collection.
