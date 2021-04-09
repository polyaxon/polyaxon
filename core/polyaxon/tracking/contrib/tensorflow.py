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
from polyaxon.tracking.contrib.tensorboard import PolyaxonTensorboardLogger

try:
    import tensorflow as tf
except ImportError:
    raise PolyaxonClientException("tensorflow is required to use PolyaxonCallback")

SessionRunHook = None

try:
    from tensorflow.train import SessionRunHook  # noqa
except ImportError:
    pass

if not SessionRunHook:
    raise PolyaxonClientException("tensorflow is required to use PolyaxonCallback")


class PolyaxonCallback(SessionRunHook):
    def __init__(
        self,
        summary_op=None,
        steps_per_log=1000,
        run=None,
        log_image: bool = False,
        log_histo: bool = False,
        log_tensor: bool = False,
    ):
        self._summary_op = summary_op
        self._steps_per_log = steps_per_log
        self.run = tracking.get_or_create_run(run)
        self._log_image = log_image
        self._log_histo = log_histo
        self._log_tensor = log_tensor

    def begin(self):
        if self._summary_op is None:
            self._summary_op = tf.summary.merge_all()
        self._step = -1

    def before_run(self, run_context):
        self._step += 1
        return tf.train.SessionRunArgs({"summary": self._summary_op})

    def after_run(self, run_context, run_values):
        if self._step % self._steps_per_log == 0:
            PolyaxonTensorboardLogger.process_summary(
                run_values.results["summary"],
                run=self.run,
                log_image=self._log_image,
                log_histo=self._log_histo,
                log_tensor=self._log_tensor,
            )


PolyaxonSessionRunHook = PolyaxonCallback
