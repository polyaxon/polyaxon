<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/rl/base.py#L296)</span>
## BasePGModel

```python
polyaxon.models.rl.base.BasePGModel(mode, graph_fn, num_states, num_actions, loss=None, optimizer=None, metrics=None, is_deterministic=False, is_continuous=False, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Model')
```

Base reinforcement learning policy gradient model class.

- __Args__:

	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

	- __graph_fn__: Graph function. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.
	- __loss__: An instance of `LossConfig`.

	- __num_states__: `int`. The number of states.

	- __num_actions__: `int`. The number of actions.

	- __optimizer__: An instance of `OptimizerConfig`. Default value `Adam`.

	- __metrics__: a list of `MetricConfig` instances.

	- __is_continuous__: `bool`. Is the model built for a continuous or discrete space.

	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.

		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.

	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.

	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.


 - __Returns__:

	`EstimatorSpec`


----

### _build_actions


```python
_build_actions(self)
```


Create the chosen action w/o sampling.

If inference mode is used the, actions are chosen directly without sampling.


----

### _build_distribution


```python
_build_distribution(self, values)
```


----

### _build_graph_fn


```python
_build_graph_fn(self)
```


Create the new graph_fn based on the one specified by the user.
- __Returns__:

	`function`. The graph function. The graph function must return a PGModelSpec.


----

### _call_graph_fn


```python
_call_graph_fn(self, features, labels=None)
```


Calls graph function.

Creates first one or two graph, i.e. train and target graphs.
Return the optimal action given an exploration policy.

If `is_dueling` is set to `True`,
then another layer is added that represents the state value.

- __Args__:

	- __inputs__: `Tensor` or `dict` of tensors



----

### _preprocess


```python
_preprocess(self, features, labels)
```


Model specific preprocessing.

- __Args__:

	- __features__: `array`, `Tensor` or `dict`. The environment states.

	if `dict` it must contain a `state` key.
	- __labels__: `dict`. A dictionary containing `action`, `reward`, `advantage`.

