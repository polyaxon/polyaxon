<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/models.py#L22)</span>
### BaseModel

```python
polyaxon.experiments.models.BaseModel(mode, name, model_type, graph_fn, loss_config, optimizer_config=None, eval_metrics_config=None, summaries='all', clip_gradients=0.5, params=None)
```

Base class for models.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __graph_fn__: Graph function. Follows the signature:
	* Args:
	* `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
	* `inputs`: the feature inputs.
- __graph_fn__: An instance of `GraphConfig`.
- __loss_config__: An instance of `LossConfig`.
- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
- __model_type__: `str`, the type of this model.
	Possible values: `regressor`, `classifier`, `generator`
- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
	Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.
- __params__: `dict`. A dictionary of hyperparameter values.

- __Returns__:
`EstimatorSpec`
