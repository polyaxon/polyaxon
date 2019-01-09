# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.intervals import CleaningIntervalsConfig, IntervalsConfig, TTLConfig


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

    def test_cleaning_intervals_config(self):
        bad_config_dicts = [
            {
                'archived': 'dsf',
            },
            {
                'archived': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                CleaningIntervalsConfig.from_dict(config_dict)

        config_dict = {
            'archived': 12,
        }
        config = CleaningIntervalsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_ttl_config(self):
        bad_config_dicts = [
            {
                'token': 'dsf',
            },
            {
                'ephemeralToken': ['dsf'],
            },
            {
                'heartbeat': 'heartbeat'
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                TTLConfig.from_dict(config_dict)

        config_dict = {
            'token': 12,
        }
        config = TTLConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'token': 12,
            'ephemeralToken': 12,
            'heartbeat': 21,
        }
        config = TTLConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
