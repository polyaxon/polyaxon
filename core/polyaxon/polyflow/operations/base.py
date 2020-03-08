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

from marshmallow import fields, validate

from polyaxon.polyflow.component.base import BaseComponent, BaseComponentSchema
from polyaxon.polyflow.conditions import ConditionSchema
from polyaxon.polyflow.parallel import ParallelMixin, ParallelSchema
from polyaxon.polyflow.schedule import ScheduleMixin, ScheduleSchema
from polyaxon.polyflow.trigger_policies import V1TriggerPolicy


class BaseOpSchema(BaseComponentSchema):
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    parallel = fields.Nested(ParallelSchema, allow_none=True)
    dependencies = fields.List(fields.Str(), allow_none=True)
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(V1TriggerPolicy.VALUES)
    )
    conditions = fields.Nested(ConditionSchema, allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseOp


class BaseOp(BaseComponent, ParallelMixin, ScheduleMixin):
    SCHEMA = BaseOpSchema
    REDUCED_ATTRIBUTES = BaseComponent.REDUCED_ATTRIBUTES + [
        "schedule",
        "parallel",
        "dependencies",
        "trigger",
        "conditions",
        "skipOnUpstreamSkip",
    ]

    def get_parallel_kind(self):
        return self.parallel.kind if self.parallel else None

    def get_schedule_kind(self):
        return self.schedule.kind if self.schedule else None
