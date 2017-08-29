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
                 path=None,
                 save_summary_steps=100,
                 save_checkpoints_secs=None,
                 save_checkpoints_steps=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000):
        self.level = level
        self.formatter = formatter
        self.path = path
        self.save_summary_steps = save_summary_steps
        self.save_checkpoints_secs = save_checkpoints_secs
        self.save_checkpoints_steps = save_checkpoints_steps
        self.keep_checkpoint_max = keep_checkpoint_max
        self.keep_checkpoint_every_n_hours = keep_checkpoint_every_n_hours
