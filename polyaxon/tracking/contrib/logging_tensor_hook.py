# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.client import settings
from polyaxon.client.exceptions import PolyaxonClientException
from polyaxon.tracking import Run

try:
    from tensorflow.train import LoggingTensorHook
except ImportError:
    raise PolyaxonClientException(
        "tensorflow is required to use PolyaxonLoggingTensorHook"
    )


class PolyaxonLoggingTensorHook(LoggingTensorHook):
    """Hook that logs data to console and Polyaxon"""

    def __init__(self, tensors, run=None, every_n_iter=None, every_n_secs=None):
        super(PolyaxonLoggingTensorHook, self).__init__(
            tensors=tensors, every_n_iter=every_n_iter, every_n_secs=every_n_secs
        )
        self.run = run
        if settings.IS_MANAGED:
            self.run = self.run or Run()

    def _log_tensors(self, tensor_values):
        super(PolyaxonLoggingTensorHook, self)._log_tensors(tensor_values)

        if not self.run:
            return
        metrics = {k: tensor_values[k] for k in self._tensors.keys()}
        self.run.log_metrics(**metrics)
