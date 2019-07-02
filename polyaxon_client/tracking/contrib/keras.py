# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import Experiment

try:
    from keras.callbacks import Callback
except ImportError:
    try:
        from tensorflow.keras.callbacks import Callback
    except ImportError:
        raise PolyaxonClientException('Keras is required to use PolyaxonKeras')


class PolyaxonKeras(Callback):

    def __init__(self, experiment=None, metrics=None):
        self.experiment = experiment
        if settings.IS_MANAGED:
            self.experiment = self.experiment or Experiment()
        self.metrics = metrics

    def on_epoch_end(self, epoch, logs=None):
        if not logs or not self.experiment:
            return
        if self.metrics:
            metrics = {metric: logs[metric] for metric in self.metrics if metric in logs}
        else:
            metrics = logs  # Log all metrics

        self.experiment.log_metrics(**metrics)
