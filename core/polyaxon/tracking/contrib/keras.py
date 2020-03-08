#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from polyaxon import settings
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.tracking import Run

try:
    from keras.callbacks import Callback
    from keras.callbacks import ModelCheckpoint
except ImportError:
    try:
        from tensorflow.keras.callbacks import Callback
        from tensorflow.python.keras.callbacks import ModelCheckpoint
    except ImportError:
        raise PolyaxonClientException(
            "Keras is required to use PolyaxonKerasCallback/PolyaxonKerasModelCheckpoint"
        )


class PolyaxonKerasCallback(Callback):
    def __init__(self, run=None, metrics=None):
        self.run = run
        if settings.CLIENT_CONFIG.is_managed:
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


class PolyaxonKerasModelCheckpoint(ModelCheckpoint):
    """Save model checkpoint with polyaxon."""

    def __init__(self, run, filepath, **kwargs):
        super().__init__(filepath, **kwargs)
        self.run = run
        if settings.CLIENT_CONFIG.is_managed:
            self.run = self.run or Run()

    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs=logs)

        if not self.run:
            return
        # log model
        self.run.log_model(path=self.filepath)
