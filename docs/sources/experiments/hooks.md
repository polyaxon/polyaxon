<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L140)</span>
## GlobalStepWaiterHook

```python
polyaxon.experiments.hooks.GlobalStepWaiterHook(wait_until_step)
```

Delay execution until global step reaches to wait_until_step.
(A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

This hook delays execution until global step reaches to `wait_until_step`. It
is used to gradually start workers in distributed settings. One example usage
would be setting `wait_until_step=int(K*log(task_id+1))` assuming that
task_id=0 is the chief.

- __Args__:
	- __wait_until_step__: an `int` shows until which global step should we wait.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L157)</span>
## FinalOpsHook

```python
polyaxon.experiments.hooks.FinalOpsHook(final_ops, final_ops_feed_dict=None)
```

A run hook which evaluates `Tensors` at the end of a session.
(A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

- __Args__:
	- __final_ops__: A single `Tensor`, a list of `Tensors` or a dictionary of names to `Tensors`.
	- __final_ops_feed_dict__: A feed dictionary to use when running `final_ops_dict`.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L85)</span>
## StepCounterHook

```python
polyaxon.experiments.hooks.StepCounterHook(every_n_steps=100, every_n_secs=None, output_dir=None, summary_writer=None)
```

Steps per second monitor.
(A mirror to tensorflow.python.training.basic_session_run_hooks CheckpointSaverHook.)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L8)</span>
## LoggingTensorHook

```python
polyaxon.experiments.hooks.LoggingTensorHook(tensors, every_n_iter=None, every_n_secs=None, formatter=None)
```

Prints the given tensors once every N local steps or once every N seconds.
(A mirror to tensorflow.python.training.basic_session_run_hooks LoggingTensorHook.)

The tensors will be printed to the log, with `INFO` severity.

- __Args__:
	- __tensors__: `dict` that maps string-valued tags to tensors/tensor names,
		or `iterable` of tensors/tensor names.
	- __every_n_iter__: `int`, print the values of `tensors` once every N local
		steps taken on the current worker.
	- __every_n_secs__: `int` or `float`, print the values of `tensors` once every N
		seconds. Exactly one of `every_n_iter` and `every_n_secs` should be
		provided.
	- __formatter__: function, takes dict of `tag`->`Tensor` and returns a string.
		If `None` uses default printing all tensors.

- __Raises__:
	- __ValueError__: if `every_n_iter` is non-positive.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L58)</span>
## CheckpointSaverHook

```python
polyaxon.experiments.hooks.CheckpointSaverHook(checkpoint_dir, save_secs=None, save_steps=None, saver=None, checkpoint_basename='model.ckpt', scaffold=None, listeners=None)
```

Saves checkpoints every N steps or seconds.
(A mirror to tensorflow.python.training.basic_session_run_hooks CheckpointSaverHook.)

- __Args__:
	- __checkpoint_dir__: `str`, base directory for the checkpoint files.
	- __save_secs__: `int`, save every N secs.
	- __save_steps__: `int`, save every N steps.
	- __saver__: `Saver` object, used for saving.
	- __checkpoint_basename__: `str`, base name for the checkpoint files.
	- __scaffold__: `Scaffold`, use to get saver object.
	- __listeners__: List of `CheckpointSaverListener` subclass instances.
		Used for callbacks that run immediately after the corresponding
		CheckpointSaverHook callbacks, only in steps where the
		CheckpointSaverHook was triggered.

- __Raises__:
	- __ValueError__: One of `save_steps` or `save_secs` should be set.
	- __ValueError__: Exactly one of saver or scaffold should be set.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L170)</span>
## StopAfterNEvalsHook

```python
polyaxon.experiments.hooks.StopAfterNEvalsHook(num_evals, log_progress=True)
```

Run hook used by the evaluation routines to run the `eval_ops` N times.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L33)</span>
## StopAtStepHook

```python
polyaxon.experiments.hooks.StopAtStepHook(num_steps=None, last_step=None)
```

Monitor to request stop at a specified step.
(A mirror to tensorflow.python.training.basic_session_run_hooks StopAtStepHook.)

This hook requests stop after either a number of steps have been
executed or a last step has been reached. Only one of the two options can be
specified.

if `num_steps` is specified, it indicates the number of steps to execute
after `begin()` is called. If instead `last_step` is specified, it
indicates the last step we want to execute, as passed to the `after_run()`
call.

- __Args__:
	- __num_steps__: Number of steps to execute.
	- __last_step__: Step after which to stop.

- __Raises__:
	- __ValueError__: If one of the arguments is invalid.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L95)</span>
## NanTensorHook

```python
polyaxon.experiments.hooks.NanTensorHook(loss_tensor, fail_on_nan_loss=True)
```

NaN Loss monitor.
(A mirror to tensorflow.python.training.basic_session_run_hooks NanTensorHook.)

Monitors loss and stops training if loss is NaN.
Can either fail with exception or just stop training.

- __Args__:
	- __loss_tensor__: `Tensor`, the loss tensor.
	- __fail_on_nan_loss__: `bool`, whether to raise exception when loss is NaN.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/hooks.py#L111)</span>
## SummarySaverHook

```python
polyaxon.experiments.hooks.SummarySaverHook(save_steps=None, save_secs=None, output_dir=None, summary_writer=None, scaffold=None, summary_op=None)
```

Saves summaries every N steps.
(A mirror to tensorflow.python.training.basic_session_run_hooks NanTensorHook.)

- __Args__:
	- __save_steps__: `int`, save summaries every N steps. Exactly one of
		`save_secs` and `save_steps` should be set.
	- __save_secs__: `int`, save summaries every N seconds.
	- __output_dir__: `string`, the directory to save the summaries to. Only used
		if no `summary_writer` is supplied.
	- __summary_writer__: `SummaryWriter`. If `None` and an `output_dir` was passed,
		one will be created accordingly.
	- __scaffold__: `Scaffold` to get summary_op if it's not provided.
	- __summary_op__: `Tensor` of type `string` containing the serialized `Summary`
		protocol buffer or a list of `Tensor`. They are most likely an output
		by TF summary methods like `tf.summary.scalar` or
		`tf.summary.merge_all`. It can be passed in as one tensor; if more
		than one, they must be passed in as a list.

- __Raises__:
	- __ValueError__: Exactly one of scaffold or summary_op should be set.
