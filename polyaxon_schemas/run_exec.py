# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class RunExecSchema(Schema):
    cmd = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunExecConfig(**data)


class RunExecConfig(BaseConfig):
    SCHEMA = RunExecSchema
    IDENTIFIER = 'run'

    def __init__(self, cmd):
        self.cmd = cmd
