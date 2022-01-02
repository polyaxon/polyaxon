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

from polyaxon.polyflow.schedules.cron import CronScheduleSchema, V1CronSchedule
from polyaxon.polyflow.schedules.datetime import (
    DateTimeScheduleSchema,
    V1DateTimeSchedule,
)
from polyaxon.polyflow.schedules.interval import (
    IntervalScheduleSchema,
    V1IntervalSchedule,
)
from polyaxon.polyflow.schedules.kinds import V1ScheduleKind
from polyaxon.schemas.base import BaseOneOfSchema


class ScheduleSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1IntervalSchedule.IDENTIFIER: IntervalScheduleSchema,
        V1CronSchedule.IDENTIFIER: CronScheduleSchema,
        V1DateTimeSchedule.IDENTIFIER: DateTimeScheduleSchema,
    }


class ScheduleMixin:
    def get_schedule_kind(self):
        raise NotImplementedError

    @property
    def has_interval_schedule(self):
        return self.get_schedule_kind() == V1IntervalSchedule.IDENTIFIER

    @property
    def has_cron_schedule(self):
        return self.get_schedule_kind() == V1CronSchedule.IDENTIFIER

    @property
    def has_datetime_schedule(self):
        return self.get_schedule_kind() == V1DateTimeSchedule.IDENTIFIER
