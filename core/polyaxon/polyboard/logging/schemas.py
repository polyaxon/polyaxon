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
from typing import List, Optional, Text

import polyaxon_sdk
import ujson

from marshmallow import ValidationError, fields

from polyaxon.polyboard.logging.parser import (
    DATETIME_REGEX,
    ISO_DATETIME_REGEX,
    timestamp_search_regex,
)
from polyaxon.polyboard.utils import validate_csv
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.utils.date_utils import parse_datetime
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
    SEPARATOR = "|"
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
                timestamp = parse_datetime(timestamp)
            except Exception as e:
                raise ValidationError("Received an invalid timestamp") from e

        return cls(
            timestamp=timestamp if timestamp else now(tzinfo=True),
            node=node,
            pod=pod,
            container=container,
            value=value,
        )

    def to_csv(self) -> str:
        values = [
            str(self.timestamp) if self.timestamp is not None else "",
            str(self.node) if self.node is not None else "",
            str(self.pod) if self.pod is not None else "",
            str(self.container) if self.container is not None else "",
            ujson.dumps(self.value) if self.value is not None else "",
        ]

        return self.SEPARATOR.join(values)


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

    @staticmethod
    def get_csv_header() -> str:
        return V1Log.SEPARATOR.join(V1Log.REDUCED_ATTRIBUTES)

    def to_csv(self):
        _logs = ["\n{}".format(e.to_csv()) for e in self.logs]
        return "".join(_logs)

    @classmethod
    def should_chunk(cls, logs: List[V1Log]):
        return len(logs) >= cls.CHUNK_SIZE

    @classmethod
    def chunk_logs(cls, logs: List[V1Log]):
        total_size = len(logs)
        for i in range(0, total_size, cls.CHUNK_SIZE):
            yield cls(logs=logs[i : i + cls.CHUNK_SIZE])

    @classmethod
    def read_csv(cls, data: str, parse_dates: bool = True) -> "V1Logs":
        import numpy as np
        import pandas as pd

        csv = validate_csv(data)
        if parse_dates:
            df = pd.read_csv(
                csv,
                sep=V1Log.SEPARATOR,
                parse_dates=["timestamp"],
            )
        else:
            df = pd.read_csv(
                csv,
                sep=V1Log.SEPARATOR,
            )

        return cls(
            logs=[
                V1Log(
                    timestamp=i.get("timestamp"),
                    node=i.get("node"),
                    pod=i.get("pod"),
                    container=i.get("container"),
                    value=ujson.loads('"{}"'.format(i.get("value"))),
                )
                for i in df.replace({np.nan: None}).to_dict(orient="records")
            ]
        )
