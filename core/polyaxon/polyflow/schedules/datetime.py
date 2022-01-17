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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.schedules.kinds import V1ScheduleKind
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class DateTimeScheduleSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1ScheduleKind.DATETIME))
    start_at = fields.DateTime(required=True)

    @staticmethod
    def schema_config():
        return V1DateTimeSchedule


class V1DateTimeSchedule(BaseConfig, polyaxon_sdk.V1DateTimeSchedule):
    """Date schedule is an interface to kick a component execution at a specific time.

    Args:
        kind: str, should be equal to `datetime`
        start_at: datetime, required

    ## YAML usage

    ```yaml
    >>> schedule:
    >>>   kind:
    >>>   startAt:
    ```

    ## Python usage

    ```python
    >>> from datetime import datetime
    >>> from polyaxon.polyflow import V1DateTimeSchedule
    >>> schedule = V1DateTimeSchedule(
    >>>   start_at=datetime(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this schedule
    is a datetime schedule.

    If you are using the python client to create the schedule,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: datetime
    ```

    ### startAt

    Optional field to set the start time for kicking the first execution,
    all following executions will be relative to this time.

    ```yaml
    >>> run:
    >>>   startAt: "2019-06-24T21:20:07+00:00"
    ```
    """

    SCHEMA = DateTimeScheduleSchema
    IDENTIFIER = V1ScheduleKind.DATETIME

    @property
    def max_runs(self):
        return 0

    @property
    def end_at(self):
        return None

    @property
    def depends_on_past(self):
        return True
