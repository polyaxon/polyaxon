<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/models.py#L259)</span>
## RegressorModel

```python
polyaxon.experiments.models.RegressorModel(mode, name, graph_fn, loss_config=None, optimizer_config=None, eval_metrics_config=None, summaries='all', clip_gradients=0.5, params=None)
```

Regressor base model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
		* `inputs`: the feature inputs.
	- __graph_fn__: An instance of `GraphConfig`.
	- __loss_config__: An instance of `LossConfig`. Default value `mean_squared_error`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.
	- __params__: `dict`. A dictionary of hyperparameter values.

- __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/models.py#L294)</span>
## ClassifierModel

```python
polyaxon.experiments.models.ClassifierModel(mode, name, graph_fn, loss_config=None, optimizer_config=None, summaries='all', eval_metrics_config=None, clip_gradients=0.5, params=None)
```

Regressor base model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
		* `inputs`: the feature inputs.
	- __graph_fn__: An instance of `GraphConfig`.
	- __loss_config__: An instance of `LossConfig`. Default value `sigmoid_cross_entropy`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.
	- __one_hot_encode__: `bool`. to one hot encode the outputs.
	- __n_classes__: `int`. The number of classes used in the one hot encoding.
	- __params__: `dict`. A dictionary of hyperparameter values.

- __Returns__:
	`EstimatorSpec`
