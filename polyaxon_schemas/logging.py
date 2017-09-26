# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate

from polyaxon_schemas.base import BaseConfig


class LoggingSchema(Schema):
    level = fields.Str(allow_none=True, validate=validate.OneOf(
        ['INFO', 'DEBUG', 'WARN', 'ERROR', 'FATAL']))
    formatter = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LoggingConfig(**data)


class LoggingConfig(BaseConfig):
    SCHEMA = LoggingSchema
    IDENTIFIER = 'logging'

    def __init__(self,
                 level='INFO',
                 formatter=None,
                 path=None):
        self.level = level
        self.formatter = formatter
        self.path = path
