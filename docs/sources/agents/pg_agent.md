<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/agents.py#L388)</span>
## PGAgent

```python
polyaxon.estimators.agents.PGAgent(model_fn, memory, optimizer_params=None, model_dir=None, config=None, params=None)
```

PGAgent class is the basic reinforcement learning policy gradient model trainer/evaluator.

	Constructs an `PGAgent` instance.

	- __Args__:
		- __model_fn__: Model function. Follows the signature:
		* Args:
			* `features`: single `Tensor` or `dict` of `Tensor`s
				 (depending on data passed to `fit`),
			* `labels`: `Tensor` or `dict` of `Tensor`s (for multi-head models).
				If mode is `Modes.PREDICT`, `labels=None` will be passed.
				If the `model_fn`'s signature does not accept `mode`,
				the `model_fn` must still be able to handle `labels=None`.
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `params`: Optional `dict` of hyperparameters.  Will receive what
				is passed to Estimator in `params` parameter. This allows
				to configure Estimators from hyper parameter tuning.
			* `config`: Optional configuration object. Will receive what is passed
				to Estimator in `config` parameter, or the default `config`.
				Allows updating things in your model_fn based on configuration
				such as `num_ps_replicas`.
			* `model_dir`: Optional directory where model parameters, graph etc
				are saved. Will receive what is passed to Estimator in
				`model_dir` parameter, or the default `model_dir`. Allows
				updating things in your model_fn that expect model_dir, such as
				training hooks.

		* Returns:
		   `EstimatorSpec`

		Supports next three signatures for the function:

			* `(features, labels, mode)`
			* `(features, labels, mode, params)`
			* `(features, labels, mode, params, config)`
			* `(features, labels, mode, params, config, model_dir)`

		- __memory__: An instance of a subclass of `BatchMemory`.
		- __model_dir__: Directory to save model parameters, graph and etc. This can
		also be used to load checkpoints from the directory into a estimator to
		continue training a previously saved model.
		- __config__: Configuration object.
		- __params__: `dict` of hyper parameters that will be passed into `model_fn`.
			  Keys are names of parameters, values are basic python types.
	- __Raises__:
		- __ValueError__: parameters of `model_fn` don't match `params`.
	

----

### train


```python
train(self, env, episodes=None, steps=None, hooks=None, max_steps=None, max_episodes=None)
```


Trains a model given an environment.

- __Args__:
	- __env__: `Environment` instance.
	- __steps__: Number of steps for which to train model. If `None`, train forever.
	'steps' works incrementally. If you call two times fit(steps=10) then
	training occurs in total 20 steps. If you don't want to have incremental
	behaviour please set `max_steps` instead. If set, `max_steps` must be
	`None`.
	- __hooks__: List of `BaseMonitor` subclass instances.
	Used for callbacks inside the training loop.
	- __max_steps__: Number of total steps for which to train model. If `None`,
	train forever. If set, `steps` must be `None`.
	- __max_episodes__: Number of total episodes for which to train model. If `None`,
	train forever. If set, `episodes` must be `None`.

	Two calls to `fit(steps=100)` means 200 training iterations.
	On the other hand, two calls to `fit(max_steps=100)` means
	that the second call will not do any iteration since first call did all 100 steps.

- __Returns__:
	`self`, for chaining.


----

### run_episode


```python
run_episode(self, env, sess, features, labels, no_run_hooks, global_step, update_episode_op, update_timestep_op, estimator_spec)
```


We need to differentiate between the `global_timestep` and `global_step`.

 The `global_step` gets updated directly by the `train_op` and has an effect
 on the training learning rate, especially if it gets decayed.

 The `global_timestep` on the other hand is related to the episode and how many times
 our agent acted. It has an effect on the exploration rate and how it's annealed.

- __Args__:
	- __env__: `Environment` instance.
	- __sess__: `MonitoredTrainingSession` instance.
	- __estimator_spec__: `EstimatorSpec` instance.

- __Returns__:
	statistics about episode.
