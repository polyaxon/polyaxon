<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/rl_experiment.py#L8)</span>
## RLExperiment

```python
polyaxon.experiments.rl_experiment.RLExperiment(agent, env, train_steps=None, train_episodes=None, first_update=5000, update_frequency=15, eval_steps=10, train_hooks=None, eval_hooks=None, eval_delay_secs=0, continuous_eval_throttle_secs=60, delay_workers_by_global_step=False, export_strategies=None, train_steps_per_iteration=100)
```

Experiment is a class containing all information needed to train an agent.

After an experiment is created (by passing an Agent for training and evaluation),
an Experiment instance knows how to invoke training and eval loops in
a sensible fashion for distributed training.


None of the functions passed to this constructor are executed at construction time.
They are stored and used when a method is executed which requires it.

- __Args__:
	- __agent__: Object implementing an Agent.
	- __train_steps__: Perform this many steps of training.  default: None, means train forever.
	- __train_episodes__: Perform this many episodes of training.  default: None, means train forever.
	- __first_update__: First timestep to calculate `loss` and `train_op`. This is related to the
		`global_timestep` variable, number of timesteps in episodes.
	- __update_frequency__: The frequency at which we should calculate `loss` and `train_op`.
		This frequency is related to the `gloabl_step` which is incremented every time
		we update the network.
	- __eval_steps__: `evaluate` runs until input is exhausted (or another exception is raised),
		or for `eval_steps` steps, if specified.
	- __train_hooks__: A list of monitors to pass to the `Agent`'s `fit` function.
	- __eval_hooks__: A list of `SessionRunHook` hooks to pass to
		the `Agent`'s `evaluate` function.
	- __eval_delay_secs__: Start evaluating after waiting for this many seconds.
	- __continuous_eval_throttle_secs__: Do not re-evaluate unless the last evaluation
		was started at least this many seconds ago for continuous_eval().
	- __delay_workers_by_global_step__: if `True` delays training workers based on global step
		instead of time.
	- __export_strategies__: A list of `ExportStrategy`s, or a single one, or None.
	- __train_steps_per_iteration__: (applies only to continuous_train_and_eval).
		Perform this many (integer) number of train steps for each training-evaluation
		iteration. With a small value, the model will be evaluated more frequently
		with more checkpoints saved. If `None`, will use a default value
		(which is smaller than `train_steps` if provided).

- __Raises__:
	- __ValueError__: if `estimator` does not implement Estimator interface,
			or if export_strategies has the wrong type.


----

### reset_export_strategies


```python
reset_export_strategies(self, new_export_strategies=None)
```


Resets the export strategies with the `new_export_strategies`.

- __Args__:
  - __new_export_strategies__: A new list of `ExportStrategy`s, or a single one,
or None.

- __Returns__:
  The old export strategies.


----

### train


```python
train(self, delay_secs=None)
```


Fit the agent.

Train the agent for `self._train_steps` steps, after waiting for `delay_secs` seconds.
If `self._train_steps` is `None`, train forever.

- __Args__:
	- __delay_secs__: Start training after this many seconds.

- __Returns__:
	The trained estimator.


----

### evaluate


```python
evaluate(self, delay_secs=None)
```


Evaluate on the evaluation data.

Runs evaluation on the evaluation data and returns the result. Runs for
`self._eval_steps` steps, or if it's `None`, then run until input is
exhausted or another exception is raised. Start the evaluation after
`delay_secs` seconds, or if it's `None`, defaults to using
`self._eval_delay_secs` seconds.

- __Args__:
	- __delay_secs__: Start evaluating after this many seconds. If `None`, defaults to using
	`self._eval_delays_secs`.

- __Returns__:
	The result of the `evaluate` call to the `Estimator`.


----

### continuous_eval


```python
continuous_eval(self, delay_secs=None, throttle_delay_secs=None, evaluate_checkpoint_only_once=True, continuous_eval_predicate_fn=None)
```


----

### continuous_eval_on_train_data


```python
continuous_eval_on_train_data(self, delay_secs=None, throttle_delay_secs=None, continuous_eval_predicate_fn=None)
```


----

### train_and_evaluate


```python
train_and_evaluate(self)
```


Interleaves training and evaluation.

This is particular useful for a "Master" task in the cloud, whose responsibility
it is to take checkpoints, evaluate those checkpoints, and write out summaries.
Participating in training as the supervisor allows such a task to accomplish
the first and last items, while performing evaluation allows for the second.

- __Returns__:
	The result of the `evaluate` call to the `Estimator` as well as the
	export results using the specified `ExportStrategy`.


----

### continuous_train_and_eval


```python
continuous_train_and_eval()
```


Interleaves training and evaluation. (experimental)

THIS FUNCTION IS EXPERIMENTAL. It may change or be removed at any time, and without warning.


The frequency of evaluation is controlled by the `train_steps_per_iteration`
(via constructor). The model will be first trained for
`train_steps_per_iteration`, and then be evaluated in turns.

This method is intended for single machine usage.

This differs from `train_and_evaluate` as follows:
  1. The procedure will have train and evaluation in turns. The model
  will be trained for a number of steps (usually smaller than `train_steps`
  if provided) and then be evaluated.  `train_and_evaluate` will train the
  model for `train_steps` (no small training iterations).

  2. Due to the different approach this schedule takes, it leads to two
  differences in resource control. First, the resources (e.g., memory) used
  by training will be released before evaluation (`train_and_evaluate` takes
  double resources). Second, more checkpoints will be saved as a checkpoint
  is generated at the end of each training iteration.

  3. As the estimator.train starts from scratch (new graph, new states for
  input, etc) at each iteration, it is recommended to have the
  `train_steps_per_iteration` larger. It is also recommended to shuffle your
  input.

Args:
  continuous_eval_predicate_fn: A predicate function determining whether to
continue after each iteration. `predicate_fn` takes the evaluation
results as its arguments. At the beginning of evaluation, the passed
eval results will be None so it's expected that the predicate function
handles that gracefully. When `predicate_fn` is not specified, this will
run in an infinite loop or exit when global_step reaches `train_steps`.

Returns:
  A tuple of the result of the `evaluate` call to the `Estimator` and the
  export results using the specified `ExportStrategy`.

Raises:
  ValueError: if `continuous_eval_predicate_fn` is neither None nor
callable.

----

### run_std_server


```python
run_std_server(self)
```


Starts a TensorFlow server and joins the serving thread.

Typically used for parameter servers.

- __Raises__:
  - __ValueError__: if not enough information is available in the estimator's
config to create a server.


----

### test


```python
test(self)
```


Tests training, evaluating and exporting the estimator for a single step.

- __Returns__:
  The result of the `evaluate` call to the `Estimator`.
