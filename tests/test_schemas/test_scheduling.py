# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.scheduling import (
    AffinityConfig,
    NodeSelectorsConfig,
    TolerationsConfig
)


class TestSchedulingConfig(TestCase):

    def test_node_selectors_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                NodeSelectorsConfig.from_dict(config_dict)

        config_dict = {
            'core': {}

        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'experiments': {
                'polyaxon.com': 'experiments'
            },
            'tensorboards': {
                'polyaxon.jobs': 'jobs',
                'polyaxon.tensorboards': 'tensorboards'
            }
        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_affinity_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                AffinityConfig.from_dict(config_dict)

        config_dict = {
            'core': {}

        }

        config = AffinityConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'experiments': {
                'podAffinity': {
                    'preferredDuringSchedulingIgnoredDuringExecution':
                        [
                            {'weight': 100},
                        ]
                }
            }
        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_tolerations_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
            {
                'core': {},
                'tensorboards': [],
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                TolerationsConfig.from_dict(config_dict)

        config_dict = {
            'core': []
        }

        config = TolerationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'core': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'experiments': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                },
                {
                    'key': 'key',
                    'operator': 'Exists',
                    'effect': 'NoSchedule',
                }
            ],
        }

        config = TolerationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
