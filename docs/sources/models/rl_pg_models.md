<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/vpg.py#L11)</span>
## VPGModel

```python
polyaxon.models.rl.vpg.VPGModel(mode, graph_fn, num_states, num_actions, loss_config=None, optimizer_config=None, eval_metrics_config=None, is_deterministic=False, is_continuous=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a vanilla policy gradient model
- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`.
	- __num_states__: `int`. The number of states.
	- __num_actions__: `int`. The number of actions.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

 - __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/trpo.py#L20)</span>
## TRPOModel

```python
polyaxon.models.rl.base.TRPOModel(mode, graph_fn, num_states, num_actions, loss_config=None, optimizer_config=None, eval_metrics_config=None, is_deterministic=False, is_continuous=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a trust region policy optimization model
- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`.
	- __num_states__: `int`. The number of states.
	- __num_actions__: `int`. The number of actions.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

 - __Returns__:
	`EstimatorSpec`
