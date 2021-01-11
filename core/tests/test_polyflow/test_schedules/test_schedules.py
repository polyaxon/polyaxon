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

import pytest

from marshmallow import ValidationError

from polyaxon.polyflow.schedules import (
    ScheduleSchema,
    V1CronSchedule,
    V1DateTimeSchedule,
    V1IntervalSchedule,
)
from polyaxon.utils.tz_utils import now
from tests.utils import BaseTestCase


@pytest.mark.polyflow_mark
class TestScheduleConfigs(BaseTestCase):
    def test_interval_schedule(self):
        config_dict = {"frequency": 2, "startAt": "foo"}
        with self.assertRaises(ValidationError):
            V1IntervalSchedule.from_dict(config_dict)

        config_dict = {"frequency": "foo", "startAt": now().isoformat()}
        with self.assertRaises(ValidationError):
            V1IntervalSchedule.from_dict(config_dict)

        config_dict = {
            "kind": "cron",
            "frequency": 2,
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
        }
        with self.assertRaises(ValidationError):
            V1IntervalSchedule.from_dict(config_dict)

        config_dict = {"frequency": 2, "startAt": now().isoformat()}
        V1IntervalSchedule.from_dict(config_dict)

        config_dict = {
            "frequency": 2,
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
        }
        V1IntervalSchedule.from_dict(config_dict)

        config_dict = {
            "kind": "interval",
            "frequency": 2,
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
            "maxRuns": 123,
            "dependsOnPast": False,
        }
        V1IntervalSchedule.from_dict(config_dict)

    def test_cron_schedule(self):
        config_dict = {"cron": 2, "startAt": "foo"}
        with self.assertRaises(ValidationError):
            V1CronSchedule.from_dict(config_dict)

        config_dict = {
            "kind": "interval",
            "cron": "0 0 * * *",
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
        }
        with self.assertRaises(ValidationError):
            V1CronSchedule.from_dict(config_dict)

        config_dict = {"cron": "0 0 * * *"}
        V1CronSchedule.from_dict(config_dict)

        config_dict = {
            "cron": "0 0 * * *",
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
        }
        V1CronSchedule.from_dict(config_dict)

        config_dict = {
            "kind": "cron",
            "cron": "0 0 * * *",
            "startAt": now().isoformat(),
            "endAt": now().isoformat(),
            "maxRuns": 123,
            "dependsOnPast": False,
        }
        V1CronSchedule.from_dict(config_dict)

    def test_date_schedule(self):
        config_dict = {"startAt": "foo"}
        with self.assertRaises(ValidationError):
            V1DateTimeSchedule.from_dict(config_dict)

        config_dict = {"kind": "datetime", "startAt": now().isoformat()}
        V1DateTimeSchedule.from_dict(config_dict).to_dict()

    def test_schedule(self):
        configs = [
            {
                "kind": "interval",
                "frequency": 2,
                "startAt": now().isoformat(),
                "endAt": now().isoformat(),
                "dependsOnPast": False,
            },
            {
                "kind": "cron",
                "cron": "0 0 * * *",
                "startAt": now().isoformat(),
                "endAt": now().isoformat(),
                "dependsOnPast": True,
            },
            {
                "kind": "datetime",
                "startAt": "2010-01-01T00:00+00:00",
            },
        ]

        ScheduleSchema().load(configs, many=True)
