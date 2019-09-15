# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class EnabledSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return EnabledConfig


class EnabledConfig(BaseConfig):
    IDENTIFIER = "enabled"
    SCHEMA = EnabledSchema
    REDUCED_ATTRIBUTES = ["enabled"]

    def __init__(self, enabled=None):
        self.enabled = enabled
