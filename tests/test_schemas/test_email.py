# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.email import EmailConfig


class TestEmailConfig(TestCase):

    def test_email_config(self):
        config_dict = {
            'host': 'dsf',
            'port': 'sdf',
            'useTls': 123,
            'hostUser': 'sdf',
            'hostPassword': 'sdf'
        }
        with self.assertRaises(ValidationError):
            EmailConfig.from_dict(config_dict)

        config_dict = {
            'host': 'dsf',
            'port': 123,
            'useTls': False,
            'hostUser': 'sdf',
            'hostPassword': 'sdf'
        }
        config = EmailConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
