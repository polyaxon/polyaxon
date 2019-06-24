# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon_schemas.polyflow.schedule import (
    CronScheduleConfig,
    IntervalScheduleConfig,
    ScheduleSchema
)


class TestScheduleConfigs(TestCase):
    def test_interval_schedule(self):
        config_dict = {'frequency': 2, 'start_at': 'foo'}
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {'frequency': 'foo', 'start_at': local_now().isoformat()}
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {'kind': 'cron',
                       'frequency': 2,
                       'start_at': local_now().isoformat(),
                       'end_at': local_now().isoformat()}
        with self.assertRaises(ValidationError):
            IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            'frequency': 2,
            'start_at': local_now().isoformat()
        }
        IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            'frequency': 2,
            'start_at': local_now().isoformat(),
            'end_at': local_now().isoformat()
        }
        IntervalScheduleConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'interval',
            'frequency': 2,
            'start_at': local_now().isoformat(),
            'end_at': local_now().isoformat(),
            'depends_on_past': False,
        }
        IntervalScheduleConfig.from_dict(config_dict)

    def test_cron_schedule(self):
        config_dict = {'cron': 2, 'start_at': 'foo'}
        with self.assertRaises(ValidationError):
            CronScheduleConfig.from_dict(config_dict)

        config_dict = {'kind': 'interval',
                       'cron': '0 0 * * *',
                       'start_at': local_now().isoformat(),
                       'end_at': local_now().isoformat()}
        with self.assertRaises(ValidationError):
            CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            'cron': '0 0 * * *',
        }
        CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            'cron': '0 0 * * *',
            'start_at': local_now().isoformat(),
            'end_at': local_now().isoformat()
        }
        CronScheduleConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'cron',
            'cron': '0 0 * * *',
            'start_at': local_now().isoformat(),
            'end_at': local_now().isoformat(),
            'depends_on_past': False,
        }
        CronScheduleConfig.from_dict(config_dict)

    def test_schedule(self):
        configs = [
            {
                'kind': 'interval',
                'frequency': 2,
                'start_at': local_now().isoformat(),
                'end_at': local_now().isoformat(),
                'depends_on_past': False,
            },
            {
                'kind': 'cron',
                'cron': '0 0 * * *',
                'start_at': local_now().isoformat(),
                'end_at': local_now().isoformat(),
                'depends_on_past': False,
            }
        ]

        ScheduleSchema().load(configs, many=True)
