# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class ServiceLevelSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    multiple = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return ServiceLevelConfig


class ServiceLevelConfig(BaseConfig):
    IDENTIFIER = "service_level"
    SCHEMA = ServiceLevelSchema
    REDUCED_ATTRIBUTES = ["enabled", "multiple"]

    def __init__(self, enabled=None, multiple=None):
        self.enabled = enabled
        self.multiple = multiple
