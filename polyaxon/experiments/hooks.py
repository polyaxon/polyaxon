# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.python.training import basic_session_run_hooks, session_run_hook
from tensorflow.python.platform import tf_logging as logging


class LoggingTensorHook(basic_session_run_hooks.LoggingTensorHook):
    """Prints the given tensors once every N local steps or once every N seconds.
    (A mirror to tensorflow.python.training.basic_session_run_hooks LoggingTensorHook.)

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
        super(LoggingTensorHook, self).__init__(tensors, every_n_iter, every_n_secs, formatter)


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


class CheckpointSaverHook(basic_session_run_hooks.CheckpointSaverHook):
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
        super(CheckpointSaverHook, self).__init__(checkpoint_dir, save_secs, save_steps, saver,
                                                  checkpoint_basename, scaffold, listeners)


class StepCounterHook(basic_session_run_hooks.StepCounterHook):
    """Steps per second monitor.
    (A mirror to tensorflow.python.training.basic_session_run_hooks CheckpointSaverHook.)
    """

    def __init__(self, every_n_steps=100, every_n_secs=None, output_dir=None, summary_writer=None):
        super(StepCounterHook, self).__init__(
            every_n_steps, every_n_secs, output_dir, summary_writer)


class NanTensorHook(basic_session_run_hooks.NanTensorHook):
    """NaN Loss monitor.
    (A mirror to tensorflow.python.training.basic_session_run_hooks NanTensorHook.)

    Monitors loss and stops training if loss is NaN.
    Can either fail with exception or just stop training.

    Args:
        loss_tensor: `Tensor`, the loss tensor.
        fail_on_nan_loss: `bool`, whether to raise exception when loss is NaN.
    """

    def __init__(self, loss_tensor, fail_on_nan_loss=True):
        super(NanTensorHook, self).__init__(loss_tensor, fail_on_nan_loss)


class SummarySaverHook(basic_session_run_hooks.SummarySaverHook):
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
        super(SummarySaverHook, self).__init__(save_steps, save_secs, output_dir, summary_writer,
                                               scaffold, summary_op)


class GlobalStepWaiterHook(basic_session_run_hooks.GlobalStepWaiterHook):
    """Delay execution until global step reaches to wait_until_step.
    (A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

    This hook delays execution until global step reaches to `wait_until_step`. It
    is used to gradually start workers in distributed settings. One example usage
    would be setting `wait_until_step=int(K*log(task_id+1))` assuming that
    task_id=0 is the chief.

    Args:
        wait_until_step: an `int` shows until which global step should we wait.
    """

    def __init__(self, wait_until_step):
        super(GlobalStepWaiterHook, self).__init__(wait_until_step)


class FinalOpsHook(basic_session_run_hooks.FinalOpsHook):
    """A run hook which evaluates `Tensors` at the end of a session.
    (A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

    Args:
        final_ops: A single `Tensor`, a list of `Tensors` or a dictionary of names to `Tensors`.
        final_ops_feed_dict: A feed dictionary to use when running `final_ops_dict`.
    """

    def __init__(self, final_ops, final_ops_feed_dict=None):
        super(FinalOpsHook, self).__init__(final_ops, final_ops_feed_dict)


class StopAfterNEvalsHook(session_run_hook.SessionRunHook):
    """Run hook used by the evaluation routines to run the `eval_ops` N times."""

    def __init__(self, num_evals, log_progress=True):
        """Constructs the run hook.

        Args:
            num_evals: The number of evaluations to run for.
            log_progress: Whether to log evaluation progress, defaults to True.
        """
        # The number of evals to run for.
        self._num_evals = num_evals
        self._evals_completed = None
        self._log_progress = log_progress

    def _set_evals_completed_tensor(self, updated_eval_step):
        self._evals_completed = updated_eval_step

    def before_run(self, run_context):
        return session_run_hook.SessionRunArgs({
            'evals_completed': self._evals_completed
        })

    def after_run(self, run_context, run_values):
        evals_completed = run_values.results['evals_completed']
        if self._log_progress:
            logging.info('Evaluation [%d/%d]', evals_completed, self._num_evals)
        if evals_completed >= self._num_evals:
            run_context.request_stop()


HOOKS = {
    'LoggingTensorHook': LoggingTensorHook,
    'StopAtStepHook': StopAtStepHook,
    'CheckpointSaverHook': CheckpointSaverHook,
    'StepCounterHook': StepCounterHook,
    'NanTensorHook': NanTensorHook,
    'SummarySaverHook': SummarySaverHook,
    'GlobalStepWaiterHook': GlobalStepWaiterHook,
    'FinalOpsHook': FinalOpsHook,
    'StopAfterNEvalsHook': StopAfterNEvalsHook
}
