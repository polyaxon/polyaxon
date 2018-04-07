# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email(allow_none=True)
    is_superuser = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return UserConfig(**data)

    @post_dump
    def unmake(self, data):
        return UserConfig.remove_reduced_attrs(data)


class UserConfig(BaseConfig):
    SCHEMA = UserSchema
    IDENTIFIER = 'user'

    def __init__(self, username, email, is_superuser=False):
        self.username = username
        self.email = email
        self.is_superuser = is_superuser
