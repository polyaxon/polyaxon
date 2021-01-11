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
    raise PolyaxonClientException(
        "tensorflow is required to use PolyaxonLoggingTensorHook"
    )

LoggingTensorHook = None
SessionRunHook = None

try:
    from tensorflow.train import LoggingTensorHook, SessionRunHook  # noqa
except ImportError:
    pass

try:
    from tensorflow.estimator import LoggingTensorHook, SessionRunHook  # noqa
except ImportError:
    pass

if not LoggingTensorHook or not SessionRunHook:
    raise PolyaxonClientException(
        "tensorflow is required to use PolyaxonLoggingTensorHook"
    )


class PolyaxonLoggingTensorHook(LoggingTensorHook):
    """Hook that logs data to console and Polyaxon"""

    def __init__(self, tensors, run=None, every_num_iterations=None, every_n_secs=None):
        super().__init__(
            tensors=tensors,
            every_num_iterations=every_num_iterations,
            every_n_secs=every_n_secs,
        )
        self.run = tracking.get_or_create_run(run)

    def _log_tensors(self, tensor_values):
        super()._log_tensors(tensor_values)

        if not self.run:
            return
        metrics = {k: tensor_values[k] for k in self._tensors.keys()}
        self.run.log_metrics(**metrics)


class PolyaxonSessionRunHook(SessionRunHook):
    def __init__(self, summary_op=None, steps_per_log=1000, run=None):
        self._summary_op = summary_op
        self._steps_per_log = steps_per_log
        self.run = tracking.get_or_create_run(run)

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
                run_values.results["summary"], run=self.run
            )
