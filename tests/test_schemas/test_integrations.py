# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.integrations import IntegrationsConfig


class TestIntegrationConfig(TestCase):

    def test_integrations_config(self):
        bad_config_dicts = [
            {
                'slack': 'dsf',
            },
            {
                'hipchat': 'dsf',
            },
            {
                'mattermost': 'dsf',
            },
            {
                'discord': 'dsf',
            },
            {
                'pagerduty': 'dsf',
            },
            {
                'webhooks': 'dsf',
            },
            {
                'webhooks': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                IntegrationsConfig.from_dict(config_dict)

        config_dict = {
            'slack': [{'url': 'dsf'}, {'url': 'dsf'}],
            'webhooks': [{'url': 'dsf'}, {'url': 'dsf'}],
        }
        config = IntegrationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
