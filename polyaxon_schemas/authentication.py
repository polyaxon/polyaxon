# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class AccessTokenSchema(Schema):
    username = fields.Str()
    token = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AccessTokenConfig(**data)


class AccessTokenConfig(BaseConfig):
    SCHEMA = AccessTokenSchema
    IDENTIFIER = 'token'

    def __init__(self, username, token):
        self.username = username
        self.token = token


class CredentialsSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make(self, data):
        return CredentialsConfig(**data)


class CredentialsConfig(BaseConfig):
    SCHEMA = CredentialsSchema
    IDENTIFIER = 'credentials'

    def __init__(self, username, password):
        self.username = username
        self.password = password
