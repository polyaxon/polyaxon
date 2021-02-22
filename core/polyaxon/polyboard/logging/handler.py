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
import os
import socket

from polyaxon import settings
from polyaxon.env_vars.keys import POLYAXON_KEYS_K8S_NODE_NAME, POLYAXON_KEYS_K8S_POD_ID
from polyaxon.logger import logger
from polyaxon.polyboard.logging import V1Log
from polyaxon.utils.date_utils import to_datetime
from polyaxon.utils.env import get_user


class PolyaxonHandler(logging.Handler):
    def __init__(self, add_logs, **kwargs):
        self._add_logs = add_logs
        self._container = socket.gethostname()
        self._node = os.environ.get(POLYAXON_KEYS_K8S_NODE_NAME, "local")
        self._pod = os.environ.get(POLYAXON_KEYS_K8S_POD_ID, get_user())
        super().__init__(
            level=kwargs.get(
                "level", settings.CLIENT_CONFIG.log_level or logging.NOTSET
            ),
        )

    def set_add_logs(self, add_logs):
        self._add_logs = add_logs

    def can_record(self, record):
        return not (
            record.name == "polyaxon"
            or record.name == "polyaxon.cli"
            or record.name.startswith("polyaxon")
        )

    def format_record(self, record):
        message = ""
        if record.msg:
            message = record.msg % record.args
        return V1Log.process_log_line(
            value=message,
            timestamp=to_datetime(record.created),
            node=self._node,
            pod=self._pod,
            container=self._container,
        )

    def emit(self, record):  # pylint:disable=inconsistent-return-statements
        if not self.can_record(record):
            return
        try:
            return self._add_logs(self.format_record(record))
        except Exception as e:
            logger.warning("Polyaxon failed creating log record %e", e)
