<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/base.py#L21) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/models.py#L21)</span>
## BaseModel

```python
polyaxon.models.base.BaseModel(mode, model_type, graph_fn, loss, optimizer=None, metrics=None, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```


----

### _clip_gradients_fn


```python
_clip_gradients_fn(self, grads_and_vars)
```


Clips gradients by global norm.

----

### _build_optimizer


```python
_build_optimizer(self)
```


Creates the optimizer

----

### _build_summary_op


```python
_build_summary_op(self, results=None, features=None, labels=None)
```


Builds summaries for this model.

The summaries are one value (or more) of:
	* (`ACTIVATIONS`, `VARIABLES`, `GRADIENTS`, `LOSS`, `LEARNING_RATE`)


----

### _build_loss


```python
_build_loss(self, results, features, labels)
```


Creates the loss operation

- __Returns__:

	 tuple `(losses, loss)`:
	`losses` are the per-batch losses.
	`loss` is a single scalar tensor to minimize.


----

### _build_eval_metrics


```python
_build_eval_metrics(self, results, features, labels)
```


Creates the loss operation

Returns a tuple `(losses, loss)`:
	`losses` are the per-batch losses.
	`loss` is a single scalar tensor to minimize.


----

### _build_train_op


```python
_build_train_op(self, loss)
```


Creates the training operation

----

### _preprocess


```python
_preprocess(self, features, labels)
```


Model specific preprocessing.

----

### _build_predictions


```python
_build_predictions(self, results, features, labels)
```


Creates the dictionary of predictions that is returned by the model.

----

### _build


```python
_build(self, features, labels, params=None, config=None)
```


Build the different operation of the model.

----

### batch_size


```python
batch_size(features, labels)
```


Returns the batch size of the current batch based on the passed features.

- __Args__:

	- __features__: The features.

	- __labels__: The labels

