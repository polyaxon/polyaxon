# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ml.hooks import HookSchema
from polyaxon_schemas.ml.processing.pipelines import PipelineSchema


class TrainSchema(BaseSchema):
    data_pipeline = fields.Nested(PipelineSchema)
    steps = fields.Int(allow_none=True)
    hooks = fields.Nested(HookSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return TrainConfig


class TrainConfig(BaseConfig):
    SCHEMA = TrainSchema
    IDENTIFIER = 'train'

    def __init__(self, data_pipeline, steps=100, hooks=None):
        self.data_pipeline = data_pipeline
        self.hooks = hooks
        self.steps = steps
