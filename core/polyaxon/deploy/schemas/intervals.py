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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class IntervalsSchema(BaseCamelSchema):
    runs_scheduler = fields.Int(default=None)
    operations_default_retry_delay = fields.Int(default=None)
    operations_max_retry_delay = fields.Int(default=None)
    compatibility_check = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return IntervalsConfig


class IntervalsConfig(BaseConfig):
    SCHEMA = IntervalsSchema
    REDUCED_ATTRIBUTES = [
        "runsScheduler",
        "operationsDefaultRetryDelay",
        "operationsMaxRetryDelay",
        "compatibilityCheck",
    ]

    def __init__(
        self,  # noqa
        runs_scheduler=None,
        operations_default_retry_delay=None,
        operations_max_retry_delay=None,
        compatibility_check=None,
    ):
        self.runs_scheduler = runs_scheduler
        self.operations_default_retry_delay = operations_default_retry_delay
        self.operations_max_retry_delay = operations_max_retry_delay
        self.compatibility_check = compatibility_check
