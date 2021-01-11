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
from polyaxon.logger import logger
from polyaxon.polyboard.logging import V1Log


class PolyaxonHandler(logging.Handler):
    def __init__(self, send_logs, **kwargs):
        self._send_logs = send_logs
        logging.Handler.__init__(
            self,
            level=kwargs.get(
                "level", settings.CLIENT_CONFIG.log_level or logging.NOTSET
            ),
        )

    def set_send_logs(self, send_logs):
        self._send_logs = send_logs

    def can_record(self, record):
        return not (
            record.name == "polyaxon"
            or record.name == "polyaxon.cli"
            or record.name.startswith("polyaxon")
        )

    def format_record(self, record):
        return V1Log(value=record.msg)

    def emit(self, record):  # pylint:disable=inconsistent-return-statements
        if settings.CLIENT_CONFIG.is_managed or not self.can_record(record):
            return
        try:
            return self._send_logs(self.format_record(record))
        except Exception:
            logger.warning("Polyaxon failed creating log record")
