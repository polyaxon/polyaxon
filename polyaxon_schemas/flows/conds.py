# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon_schemas.flows.trigger_policies import ExpressionTriggerPolicy, StatusTriggerPolicy


class StatusCondSchema(BaseSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('status_cond'))
    op = fields.Str()
    trigger = fields.Str(allow_none=True, validate=validate.OneOf(StatusTriggerPolicy.VALUES))

    @staticmethod
    def schema_config():
        return StatusCondConfig


class StatusCondConfig(BaseConfig):
    SCHEMA = StatusCondSchema
    IDENTIFIER = 'status_cond'

    def __init__(self, op, trigger, kind=None):
        self.op = op
        self.trigger = trigger
        self.kind = kind


class OutputsCondSchema(BaseSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('outputs_cond'))
    op = fields.Str()
    exp = fields.Str(allow_none=True, validate=validate.OneOf(ExpressionTriggerPolicy.VALUES))
    params = env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)))

    @staticmethod
    def schema_config():
        return OutputsCondConfig


class OutputsCondConfig(BaseConfig):
    SCHEMA = OutputsCondSchema
    IDENTIFIER = 'outputs_cond'

    def __init__(self, op, exp, params, kind=None):
        self.op = op
        self.exp = exp
        self.params = params
        self.kind = kind


class CondSchema(BaseOneOfSchema):
    TYPE_FIELD = 'kind'
    TYPE_FIELD_remove = False
    SCHEMAS = {
        StatusCondConfig.IDENTIFIER: StatusCondSchema,
        OutputsCondConfig.IDENTIFIER: OutputsCondSchema,
    }
