# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.intervals import IntervalsConfig


class TestIntervalsConfig(TestCase):
    def test_intervals_config(self):
        bad_config_dicts = [
            {
                'experimentsScheduler': 'dsf',
            },
            {
                'experimentsSync': 'dsf',
            },
            {
                'clustersUpdateSystemInfo': 'dsf',
            },
            {
                'clustersUpdateSystemNodes': 'dsf',
            },
            {
                'operationsDefaultRetryDelay': 'dsf',
            },
            {
                'operationsMaxRetryDelay': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                IntervalsConfig.from_dict(config_dict)

        config_dict = {
            'experimentsScheduler': 12,
            'experimentsSync': 12,
            'clustersUpdateSystemInfo': 12,
            'clustersUpdateSystemNodes': 12,
            'pipelinesScheduler': 12,
            'operationsDefaultRetryDelay': 12,
            'operationsMaxRetryDelay': 12,
        }
        config = IntervalsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
