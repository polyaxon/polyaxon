# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema


class BaseMemorySchema(BaseSchema):
    size = fields.Int(allow_none=True)
    batch_size = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseMemoryConfig


class BaseMemoryConfig(BaseConfig):
    IDENTIFIER = 'Memory'
    SCHEMA = BaseMemorySchema

    def __init__(self, size=5000, batch_size=5000):
        self.size = size
        self.batch_size = batch_size


class BatchMemorySchema(BaseMemorySchema):

    @staticmethod
    def schema_config():
        return BatchMemoryConfig


class BatchMemoryConfig(BaseMemoryConfig):
    IDENTIFIER = 'BatchMemory'
    SCHEMA = BatchMemorySchema


class MemorySchema(BaseMultiSchema):
    __multi_schema_name__ = 'memory'
    __configs__ = {
        BaseMemoryConfig.IDENTIFIER: BaseMemoryConfig,
        BatchMemoryConfig.IDENTIFIER: BatchMemoryConfig,
    }
