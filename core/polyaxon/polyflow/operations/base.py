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
from typing import Dict, Set

from marshmallow import fields, validate

from polyaxon.contexts import refs as contexts_refs
from polyaxon.lifecycle import V1Statuses
from polyaxon.polyflow.component.base import BaseComponent, BaseComponentSchema
from polyaxon.polyflow.events import EventTriggerSchema, V1EventKind
from polyaxon.polyflow.joins import JoinSchema
from polyaxon.polyflow.matrix import MatrixMixin, MatrixSchema
from polyaxon.polyflow.schedules import ScheduleMixin, ScheduleSchema
from polyaxon.polyflow.trigger_policies import V1TriggerPolicy


class BaseOpSchema(BaseComponentSchema):
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    events = fields.List(fields.Nested(EventTriggerSchema), allow_none=True)
    matrix = fields.Nested(MatrixSchema, allow_none=True)
    joins = fields.List(fields.Nested(JoinSchema), allow_none=True)
    dependencies = fields.List(fields.Str(), allow_none=True)
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(V1TriggerPolicy.allowable_values)
    )
    conditions = fields.Str(allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseOp


class BaseOp(BaseComponent, MatrixMixin, ScheduleMixin):
    SCHEMA = BaseOpSchema
    REDUCED_ATTRIBUTES = BaseComponent.REDUCED_ATTRIBUTES + [
        "schedule",
        "events",
        "matrix",
        "joins",
        "dependencies",
        "trigger",
        "conditions",
        "skipOnUpstreamSkip",
    ]

    FIELDS_SAME_KIND_PATCH = ["schedule", "matrix"]

    def get_matrix_kind(self):
        return self.matrix.kind if self.matrix else None

    def get_schedule_kind(self):
        return self.schedule.kind if self.schedule else None

    def get_upstream_statuses_events(self, upstream: Set) -> Dict[str, V1Statuses]:
        statuses_by_refs = {u: [] for u in upstream}
        events = self.events or []  # type: List[V1EventTrigger]
        for e in events:
            entity_ref = contexts_refs.get_entity_ref(e.ref)
            if not entity_ref:
                continue
            if entity_ref not in statuses_by_refs:
                continue
            for kind in e.kinds:
                status = V1EventKind.events_statuses_mapping.get(kind)
                if status:
                    statuses_by_refs[entity_ref].append(status)

        return statuses_by_refs

    def has_events_for_upstream(self, upstream: str) -> bool:
        events = self.events or []  # type: List[V1EventTrigger]
        for e in events:
            entity_ref = contexts_refs.get_entity_ref(e.ref)
            if not entity_ref:
                continue
            if entity_ref == upstream:
                return True

        return False
