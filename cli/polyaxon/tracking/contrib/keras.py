#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

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
        raise PolyaxonClientException("Keras is required to use PolyaxonKeras")


class PolyaxonKeras(Callback):
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
