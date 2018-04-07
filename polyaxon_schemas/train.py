# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.hooks import HookSchema
from polyaxon_schemas.processing.pipelines import PipelineSchema


class TrainSchema(Schema):
    data_pipeline = fields.Nested(PipelineSchema)
    steps = fields.Int(allow_none=True)
    hooks = fields.Nested(HookSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return TrainConfig(**data)

    @post_dump
    def unmake(self, data):
        return TrainConfig.remove_reduced_attrs(data)


class TrainConfig(BaseConfig):
    SCHEMA = TrainSchema
    IDENTIFIER = 'train'

    def __init__(self, data_pipeline, steps=100, hooks=None):
        self.data_pipeline = data_pipeline
        self.hooks = hooks
        self.steps = steps
