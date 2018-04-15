# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig


class RunExecSchema(Schema):
    image = fields.Str()
    cmd = fields.Str(allow_none=True)
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    git = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunExecConfig(**data)

    @post_dump
    def unmake(self, data):
        return RunExecConfig.remove_reduced_attrs(data)


class RunExecConfig(BaseConfig):
    SCHEMA = RunExecSchema
    IDENTIFIER = 'run'
    REDUCED_ATTRIBUTES = ['build_steps', 'env_vars', 'git']

    def __init__(self, image, cmd=None, build_steps=None, env_vars=None, git=None):
        self.cmd = cmd
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.git = git
