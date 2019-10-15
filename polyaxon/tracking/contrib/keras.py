# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon.client import settings
from polyaxon.client.exceptions import PolyaxonClientException
from polyaxon.tracking import Run

try:
    from keras.callbacks import Callback
    from keras.callbacks import ModelCheckpoint
except ImportError:
    try:
        from tensorflow.keras.callbacks import Callback
        from tensorflow.python.keras.callbacks import ModelCheckpoint
    except ImportError:
        raise PolyaxonClientException("Keras is required to use PolyaxonKeras")


class PolyaxonKeras(Callback):
    def __init__(self, run=None, metrics=None):
        self.run = run
        if settings.IS_MANAGED:
            self.run = self.run or Run()
        self.metrics = metrics

    def on_epoch_end(self, epoch, logs=None):
        if not logs or not self.run:
            return
        if self.metrics:
            metrics = {
                metric: logs[metric] for metric in self.metrics if metric in logs
            }
        else:
            metrics = logs  # Log all metrics

        self.run.log_metrics(**metrics)


class PolyaxonModelCheckpoint(ModelCheckpoint):
    """Save model checkpoint with polyaxon."""

    def __init__(self, run, filepath, **kwargs):
        super(PolyaxonModelCheckpoint, self).__init__(filepath, **kwargs)
        self.run = run

    def on_epoch_end(self, epoch, logs=None):
        super(PolyaxonModelCheckpoint, self).on_epoch_end(epoch, logs=logs)

        # Upload files with polyaxon.
        if self.run.get_run_info():
            if os.path.isdir(self.filepath):
                self.run.log_outputs(self.filepath)
            elif os.path.isfile(self.filepath):
                self.run.log_output(self.filepath)
            else:
                raise ValueError("Unknow file type: ", self.filepath)
