# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.auth import AuthConfig, BaseAuthConfig


class TestAuthConfig(TestCase):

    def test_base_auth_config(self):
        config_dict = {}
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        with self.assertRaises(ValidationError):
            config_dict = {'enabled': True}
            BaseAuthConfig.from_dict(config_dict)

        config_dict = {'enabled': False, 'clientId': 'sdf', 'clientSecret': 'dsf'}
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {'enabled': False, 'clientId': 'sdf'}
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {'enabled': False}
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {'enabled': True, 'clientId': 'sdf', 'clientSecret': 'dsf'}
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'enabled': True,
            'clientId': 'sdf',
            'clientSecret': 'dsf',
        }
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'enabled': True,
            'clientId': 'sdf',
            'clientSecret': 'dsf',
            'url': 'dsf'
        }
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'enabled': True,
            'clientId': 'sdf',
            'clientSecret': 'dsf',
            'tenantId': 'dsf'
        }
        config = BaseAuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_auth_config(self):
        config_dict = {
            'github': {},
            'gitlab': {'enabled': False},
            'bitbucket': {'clientId': 'sdf'},
            'azure': {'enabled': False, 'clientId': 'sdf'},
        }

        config = AuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict['github'] = {
            'enabled': True,
            'clientId': 'sdf',
            'clientSecret': 'dsf',
        }
        config = AuthConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict['gitlab']['enabled'] = True
        with self.assertRaises(ValidationError):
            AuthConfig.from_dict(config_dict)
