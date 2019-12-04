#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon.schemas.polyflow.schedule import (
    CronScheduleConfig,
    ExactTimeScheduleConfig,
    IntervalScheduleConfig,
    RepeatableScheduleConfig,
    ScheduleSchema,
)


@pytest.mark.polyflow_mark
class TestScheduleConfigs(TestCase):
    def test_interval_schedule(self):
        config_dict = {"frequency": 2, "start_at": "foo"}
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {"frequency": "foo", "start_at": local_now().isoformat()}
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            "kind": "cron",
            "frequency": 2,
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
        }
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {"frequency": 2, "start_at": local_now().isoformat()}
        IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            "frequency": 2,
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
        }
        IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            "kind": "interval",
            "frequency": 2,
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
            "depends_on_past": False,
        }
        IntervalScheduleConfig.from_dict(config_dict)

    def test_cron_schedule(self):
        config_dict = {"cron": 2, "start_at": "foo"}
        with self.assertRaises(ValidationError):
            CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            "kind": "interval",
            "cron": "0 0 * * *",
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
        }
        with self.assertRaises(ValidationError):
            CronScheduleConfig.from_dict(config_dict)

        config_dict = {"cron": "0 0 * * *"}
        CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            "cron": "0 0 * * *",
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
        }
        CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            "kind": "cron",
            "cron": "0 0 * * *",
            "start_at": local_now().isoformat(),
            "end_at": local_now().isoformat(),
            "depends_on_past": False,
        }
        CronScheduleConfig.from_dict(config_dict)

    def test_exact_time_schedule(self):
        config_dict = {"start_at": "foo"}
        with self.assertRaises(ValidationError):
            ExactTimeScheduleConfig.from_dict(config_dict)

        config_dict = {"kind": "exact_time", "start_at": local_now().isoformat()}
        ExactTimeScheduleConfig.from_dict(config_dict).to_dict()

    def test_repeatable_schedule(self):
        config_dict = {"limit": "foo"}
        with self.assertRaises(ValidationError):
            RepeatableScheduleConfig.from_dict(config_dict)

        config_dict = {"kind": "repeatable", "limit": 123, "depends_on_past": False}
        assert RepeatableScheduleConfig.from_dict(config_dict).to_dict() == config_dict

    def test_schedule(self):
        configs = [
            {
                "kind": "interval",
                "frequency": 2,
                "start_at": local_now().isoformat(),
                "end_at": local_now().isoformat(),
                "depends_on_past": False,
            },
            {
                "kind": "cron",
                "cron": "0 0 * * *",
                "start_at": local_now().isoformat(),
                "end_at": local_now().isoformat(),
                "depends_on_past": False,
            },
        ]

        ScheduleSchema().load(configs, many=True)
