# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class SSLSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    secretName = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return SSLConfig


class SSLConfig(BaseConfig):
    SCHEMA = SSLSchema
    REDUCED_ATTRIBUTES = ['enabled']

    def __init__(self, enabled=None, secretName=None, path=None):  # noqa
        self.enabled = enabled
        self.secretName = secretName
        self.path = path
