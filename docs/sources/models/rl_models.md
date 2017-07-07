<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/dqn.py#L12)</span>
## DQNModel

```python
polyaxon.models.rl.base.DQNModel(mode, graph_fn, num_states, num_actions, loss_config=None, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, target_update_frequency=5, is_continuous=False, dueling='mean', use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a double deep Q model.

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
	- __discount__: `float`. The discount factor on the target Q values.
	- __exploration_config__: An instance `ExplorationConfig`
	- __use_target_graph__: `bool`. To use a second “target” network,
		which we will use to compute target Q values during our updates.
	- __update_frequency__: `int`. At which frequency to update the target graph.
		Only used when `use_target_graph` is set tot True.
	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.
	- __dueling__: `str` or `bool`. To compute separately the advantage and value functions.
		- __Options__:
		* `True`: creates advantage and state value without any further computation.
		* `mean`, `max`, and `naive`: creates advantage and state value, and computes
		  Q = V(s) + A(s, a)
		  where A = A - mean(A) or A = A - max(A) or A = A.
	- __use_expert_demo__: Whether to pretrain the model on a human/expert data.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

 - __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/ddqn.py#L12)</span>
## DDQNModel

```python
polyaxon.models.rl.base.DDQNModel(mode, graph_fn, num_states, num_actions, loss_config=None, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, target_update_frequency=5, is_continuous=False, dueling='mean', use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a double deep Q model.

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
	- __discount__: `float`. The discount factor on the target Q values.
	- __exploration_config__: An instance `ExplorationConfig`
	- __use_target_graph__: `bool`. To use a second “target” network,
		which we will use to compute target Q values during our updates.
	- __update_frequency__: `int`. At which frequency to update the target graph.
		Only used when `use_target_graph` is set tot True.
	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.
	- __dueling__: `str` or `bool`. To compute separately the advantage and value functions.
		- __Options__:
		* `True`: creates advantage and state value without any further computation.
		* `mean`, `max`, and `naive`: creates advantage and state value, and computes
		  Q = V(s) + A(s, a)
		  where A = A - mean(A) or A = A - max(A) or A = A.
	- __use_expert_demo__: Whether to pretrain the model on a human/expert data.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

 - __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/naf.py#L14)</span>
## NAFModel

```python
polyaxon.models.rl.naf.NAFModel(mode, graph_fn, loss_config, num_states, num_actions, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, target_update_frequency=5, is_continuous=True, use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a normalized advantage functions model.

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
	- __discount__: `float`. The discount factor on the target Q values.
	- __exploration_config__: An instance `ExplorationConfig`
	- __use_target_graph__: `bool`. To use a second “target” network,
		which we will use to compute target Q values during our updates.
	- __target_update_frequency__: `int`. At which frequency to update the target graph.
		Only used when `use_target_graph` is set tot True.
	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.
	- __use_expert_demo__: Whether to pretrain the model on a human/expert data.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

 - __Returns__:
	`EstimatorSpec`
