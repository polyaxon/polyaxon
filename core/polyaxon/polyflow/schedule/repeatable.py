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


class RepeatableScheduleSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("repeatable"))
    limit = fields.Int(required=True, validate=validate.Range(min=1))
    depends_on_past = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1RepeatableSchedule


class V1RepeatableSchedule(BaseConfig, polyaxon_sdk.V1RepeatableSchedule):
    """Repeatable schedules is an interface to trigger components repeatedly for a
    limited number of times.

    Args:
        kind: str, should be equal to `interval`
        limit: int, required
        depends_on_past: bool, optional


    ## YAML usage

    ```yaml
    >>> schedule:
    >>>   kind:
    >>>   limit:
    >>>   dependsOnPast:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1RepeatableSchedule
    >>> schedule = V1RepeatableSchedule(
    >>>   frequency=10,
    >>>   dependsOnPast=True,
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that
    this schedule is a repeatable schedule.

    If you are using the python client to create the schedule,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: repeatable
    ```

    ### limit

    The maximum number of times to execute the component.

    ```yaml
    >>> run:
    >>>   limit: 10
    ```

    ### dependsOnPast

    Optional field to tell Polyaxon to check if the
    previous execution was done before scheduling a new one, by default this is set to `false`.

    In the case where this field is set to False,
    the operations will trigger all runs at the same time.

    ```yaml
    >>> run:
    >>>   limit: 10
    ```
    """

    SCHEMA = RepeatableScheduleSchema
    IDENTIFIER = "repeatable"
