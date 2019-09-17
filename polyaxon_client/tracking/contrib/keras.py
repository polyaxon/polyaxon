# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_client import settings
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.tracking import Experiment


try:
    from keras.callbacks import Callback
    from keras.callbacks import ModelCheckpoint
except ImportError:
    try:
        from tensorflow.keras.callbacks import Callback
        from tensorflow.python.keras.callbacks import ModelCheckpoint
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


class PolyaxonModelCheckpoint(ModelCheckpoint):
    """Save model checkpoint with polyaxon."""

    def __init__(self, experiment, filepath, **kwargs):
        super(PolyaxonModelCheckpoint, self).__init__(filepath, **kwargs)
        self.experiment = experiment

    def on_epoch_end(self, epoch, logs=None):
        super(PolyaxonModelCheckpoint, self).on_epoch_end(epoch, logs=logs)

        # Upload files with polyaxon.
        if self.experiment.get_experiment_info():
            if os.path.isdir(self.filepath):
                self.experiment.log_outputs(self.filepath)
            elif os.path.isfile(self.filepath):
                self.experiment.log_output(self.filepath)
            else:
                raise ValueError("Unknow file type: ", self.filepath)
