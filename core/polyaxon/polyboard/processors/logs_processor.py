# !/usr/bin/python
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

import logging

from polyaxon.polyboard.logging.handler import PolyaxonHandler

EXCLUDE_DEFAULT_LOGGERS = ("polyaxon.client", "polyaxon.cli")


def setup_logging(add_logs, exclude=EXCLUDE_DEFAULT_LOGGERS):
    plx_logger = logging.getLogger()
    plx_logger.setLevel(logging.INFO)
    if logging.StreamHandler not in map(type, plx_logger.handlers):
        plx_logger.addHandler(logging.StreamHandler())
        plx_logger.propagate = False
    if PolyaxonHandler in map(type, plx_logger.handlers):
        for handler in plx_logger.handlers:
            if isinstance(handler, PolyaxonHandler):
                handler.set_add_logs(add_logs=add_logs)
    else:
        handler = PolyaxonHandler(add_logs=add_logs)
        plx_logger.addHandler(handler)

    for logger_name in exclude:
        plx_logger = logging.getLogger(logger_name)
        if logging.StreamHandler not in map(type, plx_logger.handlers):
            plx_logger.addHandler(logging.StreamHandler())
            plx_logger.propagate = False
