# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ml.hooks import HookSchema
from polyaxon_schemas.ml.processing.pipelines import PipelineSchema


class EvalSchema(BaseSchema):
    data_pipeline = fields.Nested(PipelineSchema)
    steps = fields.Int(allow_none=True)
    hooks = fields.Nested(HookSchema, many=True, allow_none=True)
    delay_secs = fields.Int(allow_none=True)
    continuous_eval_throttle_secs = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return EvalConfig


class EvalConfig(BaseConfig):
    SCHEMA = EvalSchema
    IDENTIFIER = 'eval'

    def __init__(self,
                 data_pipeline,
                 steps=10,
                 hooks=None,
                 delay_secs=0,
                 continuous_eval_throttle_secs=60):
        self.data_pipeline = data_pipeline
        self.steps = steps
        self.hooks = hooks
        self.delay_secs = delay_secs
        self.continuous_eval_throttle_secs = continuous_eval_throttle_secs
