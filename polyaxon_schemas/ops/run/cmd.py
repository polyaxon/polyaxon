# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.string_utils import strip_spaces
from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import ObjectOrListObject


def get_container_command_args(run_config):
    if not run_config or not run_config.cmd:
        raise ValueError('The specification must contain a command.')

    def sanitize_cmd(cmd):
        cmd = strip_spaces(value=cmd, join=False)
        cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
        cmd = [c for c in cmd if (c and c != '\\')]
        return ' '.join(cmd)

    return (
        ["/bin/bash", "-c"],
        [' && '.join([sanitize_cmd(cmd) for cmd in run_config.cmd])]
        if isinstance(run_config.cmd, list)
        else [sanitize_cmd(run_config.cmd)]
    )


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

    def get_container_cmd(self):
        return get_container_command_args(self)
