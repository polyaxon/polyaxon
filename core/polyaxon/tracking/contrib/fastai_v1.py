#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from polyaxon import tracking
from polyaxon.exceptions import PolyaxonClientException

try:
    from fastai.callbacks import TrackerCallback
except ImportError:
    raise PolyaxonClientException("Fastai is required to use PolyaxonCallback")


class PolyaxonCallback(TrackerCallback):
    def __init__(self, learn, run=None, monitor="auto", mode="auto"):
        super().__init__(learn, monitor=monitor, mode=mode)
        if monitor is None:
            # use default TrackerCallback monitor value
            super().__init__(learn, mode=mode)
        self.run = tracking.get_or_create_run(run)

    def on_epoch_end(self, epoch, smooth_loss, last_metrics, **kwargs):
        if not self.run:
            return
        metrics = {
            name: stat
            for name, stat in list(
                zip(self.learn.recorder.names, [epoch, smooth_loss] + last_metrics)
            )[1:]
        }

        self.run.log_metrics(**metrics)
