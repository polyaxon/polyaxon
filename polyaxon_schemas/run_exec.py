# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class RunSchema(Schema):
    cmd = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunConfig(**data)

    @post_dump
    def unmake(self, data):
        return RunConfig.remove_reduced_attrs(data)


class RunConfig(BaseConfig):
    SCHEMA = RunSchema
    IDENTIFIER = 'run'

    def __init__(self, cmd):
        self.cmd = cmd
