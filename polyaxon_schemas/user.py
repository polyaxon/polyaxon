# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class UserSchema(Schema):
    uuid = fields.UUID()
    username = fields.Str()
    email = fields.Email()
    type = fields.Str(allow_none=True)

    @post_load
    def make(self, data):
        return UserConfig(**data)


class UserConfig(BaseConfig):
    SCHEMA = UserSchema
    IDENTIFIER = 'user'
    REDUCED_ATTRIBUTES = ['type']

    def __init__(self, uuid, username, email, type=None):
        self.uuid = uuid
        self.username = username
        self.email = email
        self.type = type
