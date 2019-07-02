# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import Experiment

try:
    from tensorflow.train import LoggingTensorHook
except ImportError:
    raise PolyaxonClientException('tensorflow is required to use PolyaxonLoggingTensorHook')


class PolyaxonLoggingTensorHook(LoggingTensorHook):
    """Hook that logs data to console and Polyaxon"""

    def __init__(self, tensors, experiment=None, every_n_iter=None, every_n_secs=None):
        super(PolyaxonLoggingTensorHook, self).__init__(tensors=tensors,
                                                        every_n_iter=every_n_iter,
                                                        every_n_secs=every_n_secs)
        self.experiment = experiment
        if settings.IS_MANAGED:
            self.experiment = self.experiment or Experiment()

    def _log_tensors(self, tensor_values):
        super(PolyaxonLoggingTensorHook, self)._log_tensors(tensor_values)

        if not self.experiment:
            return
        metrics = {k: tensor_values[k] for k in self._tensors.keys()}
        self.experiment.log_metrics(**metrics)
