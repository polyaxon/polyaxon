# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.python.training import basic_session_run_hooks

HOOKS = {
    'LoggingTensorHook': basic_session_run_hooks.LoggingTensorHook,
    'StopAtStepHook': basic_session_run_hooks.StopAtStepHook,
    'CheckpointSaverHook': basic_session_run_hooks.CheckpointSaverHook,
    'StepCounterHook': basic_session_run_hooks.StepCounterHook,
    'NanTensorHook': basic_session_run_hooks.NanTensorHook,
    'SummarySaverHook': basic_session_run_hooks.SummarySaverHook,
}
