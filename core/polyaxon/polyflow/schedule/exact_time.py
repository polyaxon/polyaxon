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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class ExactTimeScheduleSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("exact_time"))
    start_at = fields.DateTime(required=True)

    @staticmethod
    def schema_config():
        return V1ExactTimeSchedule


class V1ExactTimeSchedule(BaseConfig, polyaxon_sdk.V1ExactTimeSchedule):
    """Exact time schedule is an interface to kick a component execution at a specific time.

    Args:
        kind: str, should be equal to `exact_time`
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
    >>> from polyaxon.polyflow import V1ExactTimeSchedule
    >>> schedule = V1ExactTimeSchedule(
    >>>   start_at=datetime(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this schedule
    is an exact time schedule.

    If you are using the python client to create the schedule,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: exect_time
    ```

    ### startAt

    Optional field to set the start time for kicking the first execution,
    all following executions will be relative to this time.

    ```yaml
    >>> run:
    >>>   startAt: "2019-06-24T21:20:07+00:00"
    ```
    """

    SCHEMA = ExactTimeScheduleSchema
    IDENTIFIER = "exact_time"
