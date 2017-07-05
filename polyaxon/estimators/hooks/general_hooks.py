# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import numpy as np

from tensorflow.python.training import basic_session_run_hooks, session_run_hook
from tensorflow.python.platform import tf_logging as logging

from polyaxon.estimators.hooks.utils import can_run_hook


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


class NanTensorHook(basic_session_run_hooks.NanTensorHook):
    """NaN Loss monitor.

    A modified version of tensorflow.python.training.basic_session_run_hooks NanTensorHook.
    Checks the context for `no_run_hooks_op` before calling the the hook.

    Monitors loss and stops training if loss is NaN.
    Can either fail with exception or just stop training.

    Args:
        loss_tensor: `Tensor`, the loss tensor.
        fail_on_nan_loss: `bool`, whether to raise exception when loss is NaN.
    """

    def __init__(self, loss_tensor, fail_on_nan_loss=True):
        """Initializes NanLoss monitor.

        Args:
          loss_tensor: `Tensor`, the loss tensor.
          fail_on_nan_loss: `bool`, whether to raise exception when loss is NaN.
        """
        self._loss_tensor = loss_tensor
        self._fail_on_nan_loss = fail_on_nan_loss

    def before_run(self, run_context):  # pylint: disable=unused-argument
        if can_run_hook(run_context):
            return super(NanTensorHook, self).before_run(run_context)
        return None

    def after_run(self, run_context, run_values):
        if can_run_hook(run_context):
            return super(NanTensorHook, self).after_run(run_context, run_values)


GENERAL_HOOKS = OrderedDict([
    ('GlobalStepWaiterHook', GlobalStepWaiterHook),
    ('FinalOpsHook', FinalOpsHook),
    ('StopAfterNEvalsHook', StopAfterNEvalsHook),
    ('NanTensorHook', NanTensorHook)
])
