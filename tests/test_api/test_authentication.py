# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.api.authentication import AccessTokenConfig, CredentialsConfig


class TestAccessConfigs(TestCase):
    def test_access_token_config(self):
        config_dict = {'username': 'username',
                       'token': 'sdfsdf098sdf80s9dSDF800'}
        config = AccessTokenConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_credentials_config(self):
        config_dict = {'username': 'username',
                       'password': 'super-secret'}
        config = CredentialsConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
