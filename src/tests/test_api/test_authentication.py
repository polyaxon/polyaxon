#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from polyaxon.env_vars.keys import POLYAXON_KEYS_AUTH_TOKEN, POLYAXON_KEYS_AUTH_USERNAME
from polyaxon.schemas.api.authentication import AccessTokenConfig, V1Credentials
from tests.utils import BaseTestCase


@pytest.mark.api_mark
class TestAccessConfigs(BaseTestCase):
    def test_access_token_config(self):
        config_dict = {
            POLYAXON_KEYS_AUTH_USERNAME: "username",
            POLYAXON_KEYS_AUTH_TOKEN: "sdfsdf098sdf80s9dSDF800",
        }
        config = AccessTokenConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_credentials_config(self):
        config_dict = {"username": "username", "password": "super-secret"}
        config = V1Credentials.from_dict(config_dict)
        assert config.to_dict() == config_dict
