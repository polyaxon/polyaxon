<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/general_hooks.py#L12)</span>
## GlobalStepWaiterHook

```python
tensorflow.python.training.basic_session_run_hooks.GlobalStepWaiterHook(wait_until_step)
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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/general_hooks.py#L28)</span>
## FinalOpsHook

```python
tensorflow.python.training.basic_session_run_hooks.FinalOpsHook(final_ops, final_ops_feed_dict=None)
```

A run hook which evaluates `Tensors` at the end of a session.
(A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

- __Args__:
	- __final_ops__: A single `Tensor`, a list of `Tensors` or a dictionary of names to `Tensors`.
	- __final_ops_feed_dict__: A feed dictionary to use when running `final_ops_dict`.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/general_hooks.py#L40)</span>
## StopAfterNEvalsHook

```python
tensorflow.python.training.evaluation.StopAfterNEvalsHook(num_evals, log_progress=True)
```

Run hook used by the evaluation routines to run the `eval_ops` N times.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/general_hooks.py#L46)</span>
## NanTensorHook

```python
tensorflow.python.training.basic_session_run_hooks.NanTensorHook(loss_tensor, fail_on_nan_loss=True)
```

NaN Loss monitor.

A modified version of tensorflow.python.training.basic_session_run_hooks NanTensorHook.
Checks the context for `no_run_hooks_op` before calling the the hook.

Monitors loss and stops training if loss is NaN.
Can either fail with exception or just stop training.

- __Args__:
	- __loss_tensor__: `Tensor`, the loss tensor.
	- __fail_on_nan_loss__: `bool`, whether to raise exception when loss is NaN.
