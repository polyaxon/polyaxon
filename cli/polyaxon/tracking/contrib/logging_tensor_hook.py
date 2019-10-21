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

from polyaxon import settings
from polyaxon.exceptions import PolyaxonClientException
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
        if settings.CLIENT_CONFIG.is_managed:
            self.run = self.run or Run()

    def _log_tensors(self, tensor_values):
        super(PolyaxonLoggingTensorHook, self)._log_tensors(tensor_values)

        if not self.run:
            return
        metrics = {k: tensor_values[k] for k in self._tensors.keys()}
        self.run.log_metrics(**metrics)
