# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class RootUserSchema(BaseSchema):
    username = fields.Str(allow_none=True, default='root')
    password = fields.Str(allow_none=True, default='rootpassword')
    email = fields.Email(allow_none=True)

    @staticmethod
    def schema_config():
        return RootUserConfig


class RootUserConfig(BaseConfig):
    SCHEMA = RootUserSchema
    REDUCED_ATTRIBUTES = ['username', 'password', 'email']

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email
