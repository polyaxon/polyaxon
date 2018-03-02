# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig


class CliConfigurationSchema(Schema):
    check_count = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return CliConfigurationConfig(**data)

    @post_dump
    def unmake(self, data):
        return CliConfigurationConfig.remove_reduced_attrs(data)


class CliConfigurationConfig(BaseConfig):
    SCHEMA = CliConfigurationSchema
    IDENTIFIER = 'cli'

    def __init__(self, check_count=0):
        self.check_count = check_count
