# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema


class TensorboardSchema(BaseRunSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('tensorboard'))

    @staticmethod
    def schema_config():
        return TensorboardConfig


class TensorboardConfig(BaseRunConfig):
    IDENTIFIER = 'tensorboard'
    SCHEMA = TensorboardSchema
