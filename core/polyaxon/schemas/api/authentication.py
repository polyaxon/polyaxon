#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import polyaxon_sdk

from marshmallow import EXCLUDE, fields

from polyaxon.env_vars.keys import POLYAXON_KEYS_AUTH_TOKEN, POLYAXON_KEYS_AUTH_USERNAME
from polyaxon.schemas.base import BaseConfig, BaseSchema


class AccessTokenSchema(BaseSchema):
    username = fields.Str(data_key=POLYAXON_KEYS_AUTH_USERNAME)
    token = fields.Str(data_key=POLYAXON_KEYS_AUTH_TOKEN)

    @staticmethod
    def schema_config():
        return AccessTokenConfig


class AccessTokenConfig(BaseConfig):
    """
    Access token config.


    Args:
        username: `str`. The user's username.
        token: `str`. The user's token.
    """

    SCHEMA = AccessTokenSchema
    IDENTIFIER = "token"

    UNKNOWN_BEHAVIOUR = EXCLUDE

    def __init__(self, username=None, token=None, **kwargs):
        self.username = username
        self.token = token


class CredentialsSchema(BaseSchema):
    username = fields.Str()
    password = fields.Str()

    @staticmethod
    def schema_config():
        return V1Credentials


class V1Credentials(BaseConfig, polyaxon_sdk.V1Credentials):
    """
    Credentials config.


    Args:
        username: `str`. The user's username.
        password: `str`. The user's password.
    """

    SCHEMA = CredentialsSchema
    IDENTIFIER = "credentials"

    def __init__(self, username, password):
        self.username = username
        self.password = password
