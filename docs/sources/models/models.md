<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/regressors.py#L12)</span>
## Regressor

```python
polyaxon.models.regressors.Regressor(mode, graph_fn, loss_config=None, optimizer_config=None, eval_metrics_config=None, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Regressor')
```

Regressor base model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
		Possible values: `regressor`, `classifier`, `generator`
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`. Default value `mean_squared_error`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

- __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/classifiers.py#L13)</span>
## Classifier

```python
polyaxon.models.classifiers.Classifier(mode, graph_fn, loss_config=None, optimizer_config=None, summaries='all', eval_metrics_config=None, clip_gradients=0.5, clip_embed_gradients=0.1, one_hot_encode=None, n_classes=None, name='Classfier')
```

Regressor base model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
		Possible values: `regressor`, `classifier`, `generator`
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`. Default value `sigmoid_cross_entropy`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __one_hot_encode__: `bool`. to one hot encode the outputs.
	- __n_classes__: `int`. The number of classes used in the one hot encoding.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

- __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/generators.py#L17)</span>
## Generator

```python
polyaxon.models.generators.Generator(mode, encoder_fn, decoder_fn, bridge_fn, loss_config=None, optimizer_config=None, summaries='all', eval_metrics_config=None, clip_gradients=0.5, clip_embed_gradients=0.1, name='Generator')
```

Generator base model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
		Possible values: `regressor`, `classifier`, `generator`.
	- __encoder_fn__: Encoder Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __decoder_fn__: Decoder Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __bridge_fn__: The bridge to use. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
		* `encoder_fn`: the encoder function.
		* `decoder_fn` the decoder function.
	- __loss_config__: An instance of `LossConfig`. Default value `mean_squared_error`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adadelta`.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.
		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.
	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.
	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.

- __Returns__:
	`EstimatorSpec`


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/dqn.py#L12)</span>
## DQNModel

```python
polyaxon.models.rl.base.DQNModel(mode, graph_fn, loss_config, env, state_preprocessing_fn=None, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, update_frequency=5, is_continuous=False, dueling='mean', use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a double deep Q model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`.
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
polyaxon.models.rl.base.DDQNModel(mode, graph_fn, loss_config, env, state_preprocessing_fn=None, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, update_frequency=5, is_continuous=False, dueling='mean', use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a double deep Q model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`.
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
polyaxon.models.rl.naf.NAFModel(mode, graph_fn, loss_config, env, state_preprocessing_fn=None, optimizer_config=None, eval_metrics_config=None, discount=0.97, exploration_config=None, use_target_graph=True, update_frequency=5, is_continuous=True, use_expert_demo=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Implements a normalized advantage functions model.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __graph_fn__: Graph function. Follows the signature:
		* Args:
		* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
		* `inputs`: the feature inputs.
	- __loss_config__: An instance of `LossConfig`.
	- __optimizer_config__: An instance of `OptimizerConfig`. Default value `Adam`.
	- __eval_metrics_config__: a list of `MetricConfig` instances.
	- __discount__: `float`. The discount factor on the target Q values.
	- __exploration_config__: An instance `ExplorationConfig`
	- __use_target_graph__: `bool`. To use a second “target” network,
		which we will use to compute target Q values during our updates.
	- __update_frequency__: `int`. At which frequency to update the target graph.
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
