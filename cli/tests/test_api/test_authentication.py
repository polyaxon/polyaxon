# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from polyaxon.env_vars.keys import POLYAXON_KEYS_AUTH_TOKEN, POLYAXON_KEYS_AUTH_USERNAME
from polyaxon.schemas.api.authentication import AccessTokenConfig, CredentialsConfig


@pytest.mark.api_mark
class TestAccessConfigs(TestCase):
    def test_access_token_config(self):
        config_dict = {
            POLYAXON_KEYS_AUTH_USERNAME: "username",
            POLYAXON_KEYS_AUTH_TOKEN: "sdfsdf098sdf80s9dSDF800",
        }
        config = AccessTokenConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_credentials_config(self):
        config_dict = {"username": "username", "password": "super-secret"}
        config = CredentialsConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
