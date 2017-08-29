# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema


class BaseMemorySchema(Schema):
    size = fields.Int(allow_none=True)
    batch_size = fields.Int(allow_none=True)

    @post_load
    def make_load(self, data):
        return BaseMemoryConfig(**data)


class BaseMemoryConfig(BaseConfig):
    IDENTIFIER = 'Memory'
    SCHEMA = BaseMemorySchema

    def __init__(self, size=5000, batch_size=5000):
        self.size = size
        self.batch_size = batch_size


class BatchMemorySchema(BaseMemorySchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return BatchMemoryConfig(**data)


class BatchMemoryConfig(BaseMemoryConfig):
    IDENTIFIER = 'BatchMemory'
    SCHEMA = BatchMemorySchema


class MemorySchema(BaseMultiSchema):
    __multi_schema_name__ = 'memory'
    __configs__ = {
        BaseMemoryConfig.IDENTIFIER: BaseMemoryConfig,
        BatchMemoryConfig.IDENTIFIER: BatchMemoryConfig,
    }
