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

import pytest

from marshmallow import ValidationError
from tests.utils import BaseTestCase

from polyaxon.polyflow.schedule import (
    ScheduleSchema,
    V1CronSchedule,
    V1ExactTimeSchedule,
    V1IntervalSchedule,
    V1RepeatableSchedule,
)
from polyaxon.utils.tz_utils import now


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
            "dependsOnPast": False,
        }
        V1CronSchedule.from_dict(config_dict)

    def test_exact_time_schedule(self):
        config_dict = {"startAt": "foo"}
        with self.assertRaises(ValidationError):
            V1ExactTimeSchedule.from_dict(config_dict)

        config_dict = {"kind": "exact_time", "startAt": now().isoformat()}
        V1ExactTimeSchedule.from_dict(config_dict).to_dict()

    def test_repeatable_schedule(self):
        config_dict = {"limit": "foo"}
        with self.assertRaises(ValidationError):
            V1RepeatableSchedule.from_dict(config_dict)

        config_dict = {"kind": "repeatable", "limit": 123, "dependsOnPast": False}
        assert V1RepeatableSchedule.from_dict(config_dict).to_dict() == config_dict

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
                "dependsOnPast": False,
            },
        ]

        ScheduleSchema().load(configs, many=True)
