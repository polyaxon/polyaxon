# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.hooks import HookSchema
from polyaxon_schemas.processing.pipelines import PipelineSchema


class EvalSchema(Schema):
    data_pipeline = fields.Nested(PipelineSchema)
    eval_steps = fields.Int(allow_none=True)
    eval_hooks = fields.Nested(HookSchema, many=True, allow_none=True)
    eval_delay_secs = fields.Int(allow_none=True)
    continuous_eval_throttle_secs = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EvalConfig(**data)


class EvalConfig(BaseConfig):
    SCHEMA = EvalSchema
    IDENTIFIER = 'eval'

    def __init__(self,
                 data_pipeline,
                 eval_steps=10,
                 eval_hooks=None,
                 eval_delay_secs=0,
                 continuous_eval_throttle_secs=60):
        self.data_pipeline = data_pipeline
        self.eval_steps = eval_steps
        self.eval_hooks = eval_hooks
        self.eval_delay_secs = eval_delay_secs
        self.continuous_eval_throttle_secs = continuous_eval_throttle_secs
