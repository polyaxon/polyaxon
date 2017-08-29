# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.hooks import HookSchema
from polyaxon_schemas.processing.pipelines import PipelineSchema


class TrainSchema(Schema):
    data_pipeline = fields.Nested(PipelineSchema)
    train_steps = fields.Int(allow_none=True)
    train_hooks = fields.Nested(HookSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return TrainConfig(**data)


class TrainConfig(BaseConfig):
    SCHEMA = TrainSchema
    IDENTIFIER = 'eval'

    def __init__(self, data_pipeline, train_steps=100, train_hooks=None):
        self.data_pipeline = data_pipeline
        self.train_hooks = train_hooks
        self.train_steps = train_steps
