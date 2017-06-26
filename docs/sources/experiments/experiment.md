<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/experiment.py#L24)</span>
## Experiment

```python
polyaxon.experiments.experiment.Experiment(estimator, train_input_fn, eval_input_fn, train_steps=None, eval_steps=10, train_hooks=None, eval_hooks=None, eval_delay_secs=0, continuous_eval_throttle_secs=60, eval_every_n_steps=1, delay_workers_by_global_step=False, export_strategies=None, train_steps_per_iteration=100)
```

Experiment is a class containing all information needed to train a model.

After an experiment is created (by passing an Estimator and inputs for
training and evaluation), an Experiment instance knows how to invoke training
and eval loops in a sensible fashion for distributed training.


None of the functions passed to this constructor are executed at construction time.
They are stored and used when a method is executed which requires it.

- __Args__:
	- __estimator__: Object implementing Estimator interface.
	- __train_input_fn__: function, returns features and labels for training.
	- __eval_input_fn__: function, returns features and labels for evaluation. If
		`eval_steps` is `None`, this should be configured only to produce for a
		finite number of batches (generally, 1 epoch over the evaluation data).
	- __train_steps__: Perform this many steps of training.  default: None, means train forever.
	- __eval_steps__: `evaluate` runs until input is exhausted (or another exception is raised),
		or for `eval_steps` steps, if specified.
	- __train_hooks__: A list of monitors to pass to the `Estimator`'s `fit` function.
	- __eval_hooks__: A list of `SessionRunHook` hooks to pass to
		the `Estimator`'s `evaluate` function.
	- __eval_delay_secs__: Start evaluating after waiting for this many seconds.
	- __continuous_eval_throttle_secs__: Do not re-evaluate unless the last evaluation
		was started at least this many seconds ago for continuous_eval().
	- __eval_every_n_steps__: (applies only to train_and_evaluate).
		the minimum number of steps between evaluations. Of course, evaluation does not
		occur if no new snapshot is available, hence, this is the minimum.
	- __delay_workers_by_global_step__: if `True` delays training workers based on global step
		instead of time.
	- __export_strategies__: A list of `ExportStrategy`s, or a single one, or None.
	- __train_steps_per_iteration__: (applies only to continuous_train_and_evaluate).
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

### extend_eval_hooks


```python
extend_eval_hooks(self, additional_hooks)
```


Extends the hooks for training.

----

### extend_eval_hooks


```python
extend_eval_hooks(self, additional_hooks)
```


Extends the hooks for training.

----

### train


```python
train(self, delay_secs=None)
```


Fit the estimator using the training data.

Train the estimator for `self._train_steps` steps, after waiting for `delay_secs` seconds.
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

The frequency of evaluation is controlled by the constructor arg `eval_every_n_steps`.
When this parameter is None or 0, evaluation happens only after training has completed.
Note that evaluation cannot happen more frequently than checkpoints are taken.
If no new snapshots are available when evaluation is supposed to occur,
then evaluation doesn't happen for another `eval_every_n_steps` steps
(assuming a checkpoint is available at that point).
Thus, settings `eval_every_n_steps` to 1 means that the model will be evaluated
everytime there is a new checkpoint.

This is particular useful for a "Master" task in the cloud, whose responsibility
it is to take checkpoints, evaluate those checkpoints, and write out summaries.
Participating in training as the supervisor allows such a task to accomplish
the first and last items, while performing evaluation allows for the second.

- __Returns__:
	The result of the `evaluate` call to the `Estimator` as well as the
	export results using the specified `ExportStrategy`.


----

### continuous_train_and_evaluate


```python
continuous_train_and_evaluate(self, continuous_eval_predicate_fn=None)
```


Interleaves training and evaluation.

The frequency of evaluation is controlled by the `train_steps_per_iteration`
(via constructor). The model will be first trained for
`train_steps_per_iteration`, and then be evaluated in turns.

This differs from `train_and_evaluate` as follows:
	1. The procedure will have train and evaluation in turns. The model
	will be trained for a number of steps (usuallly smaller than `train_steps`
	if provided) and then be evaluated.  `train_and_evaluate` will train the
	model for `train_steps` (no small training iteraions).

	2. Due to the different approach this schedule takes, it leads to two
	differences in resource control. First, the resources (e.g., memory) used
	by training will be released before evaluation (`train_and_evaluate` takes
	double resources). Second, more checkpoints will be saved as a checkpoint
	is generated at the end of each small trainning iteration.

- __Args__:
	- __continuous_eval_predicate_fn__: A predicate function determining whether to
	continue after each iteration. `predicate_fn` takes the evaluation
	results as its arguments. At the beginning of evaluation, the passed
	eval results will be None so it's expected that the predicate function
	handles that gracefully. When `predicate_fn` is not specified, this will
	run in an infinite loop or exit when global_step reaches `train_steps`.

- __Returns__:
   A tuple of the result of the `evaluate` call to the `Estimator` and the
   export results using the specified `ExportStrategy`.

- __Raises__:
	- __ValueError__: if `continuous_eval_predicate_fn` is neither None norcallable.


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


----

## create_experiment


```python
create_experiment(experiment_config)
```


Creates a new `Experiment` instance.

- __Args__:
	- __experiment_config__: the config to use for creating the experiment.


----

## run_experiment


```python
run_experiment(experiment_fn, output_dir, schedule=None)
```


Make and run an experiment.

It creates an Experiment by calling `experiment_fn`. Then it calls the
function named as `schedule` of the Experiment.

If schedule is not provided, then the default schedule for the current task
type is used. The defaults are as follows:

* 'ps' maps to 'serve'
* 'worker' maps to 'train'
* 'master' maps to 'local_run'

If the experiment's config does not include a task type, then an exception
is raised.

- __Example__:
```python
>>> def _create_my_experiment(output_dir):
>>> return tf.contrib.learn.Experiment(
>>>	 estimator=my_estimator(model_dir=output_dir),
>>>	 train_input_fn=my_train_input,
>>>	 eval_input_fn=my_eval_input)

>>> run(experiment_fn=_create_my_experiment,
>>> output_dir="some/output/dir",
>>> schedule="train")
```

- __Args__:
	- __experiment_fn__: A function that creates an `Experiment`. It should accept an
	  argument `output_dir` which should be used to create the `Estimator`
	  (passed as `model_dir` to its constructor). It must return an
	  `Experiment`.
	- __output_dir__: Base output directory.
	- __schedule__: The name of the  method in the `Experiment` to run.

- __Returns__:
	The return value of function `schedule`.

- __Raises__:
	- __ValueError__: If `output_dir` is empty, `schedule` is None but no task
	  type is set in the built experiment's config, the task type has no
	  default, or `schedule` doesn't reference a member of `Experiment`.
	- __TypeError__: `schedule` references non-callable member.
