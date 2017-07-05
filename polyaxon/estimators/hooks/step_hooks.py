# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.python.training import basic_session_run_hooks

from polyaxon.estimators.hooks.utils import can_run_hook


class StepLoggingTensorHook(basic_session_run_hooks.LoggingTensorHook):
    """Prints the given tensors once every N local steps or once every N seconds.

    A modified version of tensorflow.python.training.basic_session_run_hooks LoggingTensorHook.
    Checks the context for `no_run_hooks_op` before calling the the hook.

    The tensors will be printed to the log, with `INFO` severity.

    Args:
        tensors: `dict` that maps string-valued tags to tensors/tensor names,
            or `iterable` of tensors/tensor names.
        every_n_iter: `int`, print the values of `tensors` once every N local
            steps taken on the current worker.
        every_n_secs: `int` or `float`, print the values of `tensors` once every N
            seconds. Exactly one of `every_n_iter` and `every_n_secs` should be
            provided.
        formatter: function, takes dict of `tag`->`Tensor` and returns a string.
            If `None` uses default printing all tensors.

    Raises:
        ValueError: if `every_n_iter` is non-positive.
    """

    def __init__(self, tensors, every_n_iter=None, every_n_secs=None, formatter=None):
        super(StepLoggingTensorHook, self).__init__(tensors, every_n_iter, every_n_secs, formatter)

    def before_run(self, run_context):  # pylint: disable=unused-argument
        self._should_trigger = can_run_hook(run_context)
        if self._should_trigger:
            return super(StepLoggingTensorHook, self).before_run(run_context)
        else:
            return None


class StopAtStepHook(basic_session_run_hooks.StopAtStepHook):
    """Monitor to request stop at a specified step.
    (A mirror to tensorflow.python.training.basic_session_run_hooks StopAtStepHook.)

    This hook requests stop after either a number of steps have been
    executed or a last step has been reached. Only one of the two options can be
    specified.

    if `num_steps` is specified, it indicates the number of steps to execute
    after `begin()` is called. If instead `last_step` is specified, it
    indicates the last step we want to execute, as passed to the `after_run()`
    call.

    Args:
        num_steps: Number of steps to execute.
        last_step: Step after which to stop.

    Raises:
        ValueError: If one of the arguments is invalid.
    """

    def __init__(self, num_steps=None, last_step=None):
        super(StopAtStepHook, self).__init__(num_steps, last_step)


class StepCheckpointSaverHook(basic_session_run_hooks.CheckpointSaverHook):
    """Saves checkpoints every N steps or seconds.
    (A mirror to tensorflow.python.training.basic_session_run_hooks CheckpointSaverHook.)

    Args:
        checkpoint_dir: `str`, base directory for the checkpoint files.
        save_secs: `int`, save every N secs.
        save_steps: `int`, save every N steps.
        saver: `Saver` object, used for saving.
        checkpoint_basename: `str`, base name for the checkpoint files.
        scaffold: `Scaffold`, use to get saver object.
        listeners: List of `CheckpointSaverListener` subclass instances.
            Used for callbacks that run immediately after the corresponding
            CheckpointSaverHook callbacks, only in steps where the
            CheckpointSaverHook was triggered.

    Raises:
        ValueError: One of `save_steps` or `save_secs` should be set.
        ValueError: Exactly one of saver or scaffold should be set.
    """

    def __init__(self, checkpoint_dir, save_secs=None, save_steps=None, saver=None,
                 checkpoint_basename="model.ckpt", scaffold=None, listeners=None):
        super(StepCheckpointSaverHook, self).__init__(checkpoint_dir, save_secs, save_steps, saver,
                                                      checkpoint_basename, scaffold, listeners)


class StepCounterHook(basic_session_run_hooks.StepCounterHook):
    """Steps per second monitor.
    (A mirror to tensorflow.python.training.basic_session_run_hooks CheckpointSaverHook.)
    """

    def __init__(self, every_n_steps=100, every_n_secs=None, output_dir=None, summary_writer=None):
        super(StepCounterHook, self).__init__(
            every_n_steps, every_n_secs, output_dir, summary_writer)


class StepSummarySaverHook(basic_session_run_hooks.SummarySaverHook):
    """Saves summaries every N steps.
    (A mirror to tensorflow.python.training.basic_session_run_hooks NanTensorHook.)

    Args:
        save_steps: `int`, save summaries every N steps. Exactly one of
            `save_secs` and `save_steps` should be set.
        save_secs: `int`, save summaries every N seconds.
        output_dir: `string`, the directory to save the summaries to. Only used
            if no `summary_writer` is supplied.
        summary_writer: `SummaryWriter`. If `None` and an `output_dir` was passed,
            one will be created accordingly.
        scaffold: `Scaffold` to get summary_op if it's not provided.
        summary_op: `Tensor` of type `string` containing the serialized `Summary`
            protocol buffer or a list of `Tensor`. They are most likely an output
            by TF summary methods like `tf.summary.scalar` or
            `tf.summary.merge_all`. It can be passed in as one tensor; if more
            than one, they must be passed in as a list.

    Raises:
        ValueError: Exactly one of scaffold or summary_op should be set.
    """

    def __init__(self, save_steps=None, save_secs=None, output_dir=None, summary_writer=None,
                 scaffold=None, summary_op=None):
        super(StepSummarySaverHook, self).__init__(
            save_steps, save_secs, output_dir, summary_writer, scaffold, summary_op)


STEP_HOOKS = OrderedDict([
    ('StepLoggingTensorHook', StepLoggingTensorHook),
    ('StopAtStepHook', StopAtStepHook),
    ('StepCheckpointSaverHook', StepCheckpointSaverHook),
    ('StepCounterHook', StepCounterHook),
    ('StepSummarySaverHook', StepSummarySaverHook),
])
