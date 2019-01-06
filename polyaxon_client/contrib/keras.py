# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException

try:
    from keras.callbacks import Callback
except ImportError:
    try:
        from tensorflow.python.keras.callbacks import Callback
    except ImportError:
        raise PolyaxonClientException('Keras is required to use PolyaxonKeras')


class PolyaxonKeras(Callback):

    def __init__(self, experiment, metrics=None):
        self.experiment = experiment
        self.metrics = metrics

    def on_epoch_end(self, epoch, logs=None):
        if not logs:
            return
        if self.metrics:
            metrics = {metric: logs[metric] for metric in self.metrics if metric in logs}
        else:
            metrics = logs  # Log all metrics

        self.experiment.log_metrics(**metrics)
