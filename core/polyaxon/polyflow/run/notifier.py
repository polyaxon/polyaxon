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

from marshmallow import fields, validate

from polyaxon.polyflow.run.job import JobSchema, V1Job
from polyaxon.polyflow.run.kinds import V1RunKind


class NotifierSchema(JobSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.NOTIFIER))

    @staticmethod
    def schema_config():
        return V1Notifier


class V1Notifier(V1Job):
    SCHEMA = NotifierSchema
    IDENTIFIER = V1RunKind.NOTIFIER
