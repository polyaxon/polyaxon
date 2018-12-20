# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.utils import ObjectOrListObject


class RunSchema(BaseSchema):
    cmd = ObjectOrListObject(fields.Str)

    @staticmethod
    def schema_config():
        return RunConfig


class RunConfig(BaseConfig):
    SCHEMA = RunSchema
    IDENTIFIER = 'run'

    def __init__(self, cmd):
        self.cmd = cmd
