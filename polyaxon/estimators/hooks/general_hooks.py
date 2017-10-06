# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.python.training import basic_session_run_hooks
from tensorflow.python.training import evaluation

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

    pass


class FinalOpsHook(basic_session_run_hooks.FinalOpsHook):
    """A run hook which evaluates `Tensors` at the end of a session.
    (A mirror to tensorflow.python.training.basic_session_run_hooks GlobalStepWaiterHook.)

    Args:
        final_ops: A single `Tensor`, a list of `Tensors` or a dictionary of names to `Tensors`.
        final_ops_feed_dict: A feed dictionary to use when running `final_ops_dict`.
    """

    pass


class StopAfterNEvalsHook(evaluation._StopAfterNEvalsHook):  # pylint: disable=protected-access
    """Run hook used by the evaluation routines to run the `eval_ops` N times."""

    pass


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
