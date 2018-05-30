# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig


class BuildSchema(Schema):
    image = fields.Str()
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    git = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return BuildConfig(**data)

    @post_dump
    def unmake(self, data):
        return BuildConfig.remove_reduced_attrs(data)


class BuildConfig(BaseConfig):
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = ['build_steps', 'env_vars', 'git']

    def __init__(self, image, build_steps=None, env_vars=None, git=None):
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.git = git


class RunExecSchema(BuildSchema):
    cmd = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunExecConfig(**data)

    @post_dump
    def unmake(self, data):
        return RunExecConfig.remove_reduced_attrs(data)


class RunExecConfig(BuildConfig):
    SCHEMA = RunExecSchema
    IDENTIFIER = 'run'

    def __init__(self, image, cmd=None, build_steps=None, env_vars=None, git=None):
        self.cmd = cmd
        super(RunExecConfig, self).__init__(
            image=image,
            build_steps=build_steps,
            env_vars=env_vars,
            git=git)
