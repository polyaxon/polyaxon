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

from typing import List, Optional, Text

import polyaxon_sdk

from dateutil import parser as dt_parser
from marshmallow import ValidationError, fields

from polyaxon.polyboard.logging.parser import (
    DATETIME_REGEX,
    ISO_DATETIME_REGEX,
    timestamp_search_regex,
)
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.utils.tz_utils import now


class LogSchema(BaseSchema):
    timestamp = fields.DateTime(allow_none=True)
    node = fields.Str(allow_none=True)
    pod = fields.Str(allow_none=True)
    container = fields.Str(allow_none=True)
    value = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1Log


class V1Log(BaseConfig, polyaxon_sdk.V1Log):
    IDENTIFIER = "log"
    SCHEMA = LogSchema
    REDUCED_ATTRIBUTES = ["timestamp", "node", "pod", "container", "value"]

    @classmethod
    def process_log_line(
        cls,
        value: Text,
        node: Optional[str],
        pod: Optional[str],
        container: Optional[str],
        timestamp=None,
    ) -> "V1Log":
        if not value:
            return None

        if not isinstance(value, str):
            value = value.decode("utf-8")

        value = value.strip()

        if not timestamp:
            value, timestamp = timestamp_search_regex(ISO_DATETIME_REGEX, value)
            if not timestamp:
                value, timestamp = timestamp_search_regex(DATETIME_REGEX, value)
        if isinstance(timestamp, str):
            try:
                timestamp = dt_parser.parse(timestamp)
            except Exception as e:
                raise ValidationError("Received an invalid timestamp") from e

        return cls(
            timestamp=timestamp if timestamp else now(tzinfo=True),
            node=node,
            pod=pod,
            container=container,
            value=value,
        )


class LogsSchema(BaseSchema):
    logs = fields.List(fields.Nested(LogSchema), allow_none=True)
    last_time = fields.DateTime(allow_none=True)
    last_file = fields.Str(allow_none=True)
    files = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1Logs


class V1Logs(BaseConfig, polyaxon_sdk.V1Logs):
    CHUNK_SIZE = 2000
    IDENTIFIER = "logs"
    SCHEMA = LogsSchema
    REDUCED_ATTRIBUTES = ["logs", "last_time", "last_file", "files"]

    @classmethod
    def chunk_logs(cls, logs: List[V1Log]):
        total_size = len(logs)
        for i in range(0, total_size, cls.CHUNK_SIZE):
            yield cls(logs=logs[i : i + cls.CHUNK_SIZE])
