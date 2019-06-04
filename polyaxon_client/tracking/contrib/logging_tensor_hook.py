# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import Experiment
from polyaxon_client import settings

try:
    from tensorflow.train import LoggingTensorHook
except ImportError:
    raise PolyaxonClientException('tensorflow is required to use PolyaxonLoggingTensorHook')

class PolyaxonLoggingTensorHook(tf.train.LoggingTensorHook):
    """Hook that logs data to console and Polyaxon"""

    def __init__(self, tensors_dict, every_n_iter=None, every_n_secs=None):
        super(PolyaxonMetrics, self).__init__(tensors_dict,
                                              every_n_iter=every_n_iter,
                                              every_n_secs=every_n_secs)
        self.tensors_dict = tensors_dict.copy()

    def _log_tensors(self, tensor_values):
        super(PolyaxonMetrics, self)._log_tensors(tensor_values)
        if settings.IN_CLUSTER:
            for k in self.tensors_dict.keys():
                self.tensors_dict[k] = tensor_values[k]
            experimet = Experiment()
            experimet.log_metrics(**self.tensors_dict)
