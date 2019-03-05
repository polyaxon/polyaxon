# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class AccessTokenSchema(BaseSchema):
    username = fields.Str()
    token = fields.Str()

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
    IDENTIFIER = 'token'

    def __init__(self, username, token):
        self.username = username
        self.token = token


class CredentialsSchema(BaseSchema):
    username = fields.Str()
    password = fields.Str()

    @staticmethod
    def schema_config():
        return CredentialsConfig


class CredentialsConfig(BaseConfig):
    """
    Credentials config.


    Args:
        username: `str`. The user's username.
        password: `str`. The user's password.
    """
    SCHEMA = CredentialsSchema
    IDENTIFIER = 'credentials'

    def __init__(self, username, password):
        self.username = username
        self.password = password
