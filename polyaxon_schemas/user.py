# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class UserSchema(BaseSchema):
    username = fields.Str()
    email = fields.Email(allow_none=True)
    is_superuser = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return UserConfig


class UserConfig(BaseConfig):
    SCHEMA = UserSchema
    IDENTIFIER = 'user'

    def __init__(self, username, email, is_superuser=False):
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
