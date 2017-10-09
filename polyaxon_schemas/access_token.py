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
