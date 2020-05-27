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

import os

from polyaxon import tracking
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.logger import logger

summary_pb2 = None

try:
    from tensorflow.core.framework import summary_pb2  # noqa
except ImportError:
    pass
try:
    from tensorboardX.proto import summary_pb2  # noqa
except ImportError:
    pass

try:
    from tensorboard.compat.proto import summary_pb2  # noqa
except ImportError:
    pass

if not summary_pb2:
    raise PolyaxonClientException(
        "tensorflow/tensorboard/tensorboardx is required to use PolyaxonTensorboardLogger"
    )


class PolyaxonTensorboardLogger:
    @classmethod
    def process_summary(cls, summary, global_step=None, run=None):
        run = tracking.get_or_create_run(run)
        if not run:
            return

        if isinstance(summary, bytes):
            summary_proto = summary_pb2.Summary()
            summary_proto.ParseFromString(summary)
            summary = summary_proto

        step = cls._process_step(global_step)
        for value in summary.value:
            try:
                cls.add_value(run=run, step=step, value=value)
            except PolyaxonClientException(
                "Polyaxon failed processing tensorboard summary."
            ):
                pass

    @classmethod
    def add_value(cls, run, step, value):
        field = value.WhichOneof("value")

        if field == "simple_value":
            run.log_metric(name=value.tag, step=step, value=value.simple_value)
            return

        if field == "image":
            run.log_image(name=value.tag, step=step, data=value.image)
            return

        if (
            field == "tensor"
            and value.tensor.string_val
            and len(value.tensor.string_val)
        ):
            string_values = []
            for _ in range(0, len(value.tensor.string_val)):
                string_value = value.tensor.string_val.pop()
                string_values.append(string_value.decode("utf-8"))

                run.log_text(name=value.tag, step=step, text=", ".join(string_values))
            return

        elif field == "histo":
            if len(value.histo.bucket_limit) >= 3:
                first = (
                    value.histo.bucket_limit[0]
                    + value.histo.bucket_limit[0]
                    - value.histo.bucket_limit[1]
                )
                last = (
                    value.histo.bucket_limit[-2]
                    + value.histo.bucket_limit[-2]
                    - value.histo.bucket_limit[-3]
                )
                values, counts = (
                    list(value.histo.bucket),
                    [first] + value.histo.bucket_limit[:-1] + [last],
                )
                try:
                    run.log_np_histogram(
                        name=value.tag, values=values, counts=counts, step=step
                    )
                    return
                except ValueError:
                    logger.warning(
                        "Ignoring histogram for tag `{}`, "
                        "Histograms must have few bins".format(value.tag)
                    )
            else:
                logger.warning(
                    "Ignoring histogram for tag `{}`, "
                    "Found a histogram with only 2 bins.".format(value.tag)
                )

    @staticmethod
    def get_writer_name(log_dir):
        return os.path.basename(os.path.normpath(log_dir))

    @staticmethod
    def _process_step(global_step):
        return int(global_step) if global_step is not None else None
