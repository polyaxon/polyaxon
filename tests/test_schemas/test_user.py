# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.root_user import RootUserConfig


class TestRootUserConfig(TestCase):

    def test_root_user_config(self):
        bad_config_dicts = [
            {
                'username': False,
                'password': 'foo',
                'email': 'sdf'

            },
            {
                'username': 'sdf',
                'password': 'foo',
                'email': 'sdf'
            },
            {
                'username': 'sdf',
                'password': 'foo',
                'email': 'sdf@boo'
            },

        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                RootUserConfig.from_dict(config_dict)

        config_dict = {
            'username': 'sdf',
            'password': 'foo',

        }

        config = RootUserConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'username': 'sdf',
            'password': 'foo',
            'email': 'foo@bar.com'

        }

        config = RootUserConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
