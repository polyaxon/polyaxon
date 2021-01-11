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

import logging

from polyaxon import settings
from polyaxon.client.handlers.handler import PolyaxonHandler

EXCLUDE_DEFAULT_LOGGERS = ("polyaxon.client", "polyaxon.cli")


def setup_logging(send_logs, exclude=EXCLUDE_DEFAULT_LOGGERS):
    if settings.CLIENT_CONFIG.is_managed:
        return

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if PolyaxonHandler in map(type, logger.handlers):
        for handler in logger.handlers:
            if isinstance(handler, PolyaxonHandler):
                handler.set_send_logs(send_logs=send_logs)
    else:
        handler = PolyaxonHandler(send_logs=send_logs)

    logger.addHandler(handler)

    for logger_name in exclude:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())
