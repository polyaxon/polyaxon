# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import UUID


class DataDetailsSchema(BaseSchema):
    state = fields.Str()
    size = fields.Float()
    uri = fields.Url()

    @staticmethod
    def schema_config():
        return DataDetailsConfig


class DataDetailsConfig(BaseConfig):
    SCHEMA = DataDetailsSchema
    IDENTIFIER = 'data_details'

    def __init__(self, state, size, uri):
        self.state = state
        self.size = size
        self.uri = uri


class DataSchema(BaseSchema):
    uuid = UUID()
    name = fields.Str()
    created_at = fields.LocalDateTime()
    description = fields.Str(allow_none=True)
    details = fields.Nested(DataDetailsSchema)
    version = fields.Str(allow_none=True)
    resource_id = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return DataConfig


class DataConfig(BaseConfig):
    SCHEMA = DataSchema
    IDENTIFIER = 'data'
    DATETIME_ATTRIBUTES = ['created_at']

    def __init__(self,
                 uuid,
                 name,
                 created_at,
                 description,
                 details,
                 version=None,
                 resource_id=None):
        self.uuid = uuid
        self.name = name
        self.created_at = self.localize_date(created_at)
        self.description = description
        self.details = details
        self.version = int(float(version)) if version else None
        self.resource_id = resource_id


class DatasetSchema(BaseSchema):
    uuid = UUID()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    is_public = fields.Boolean()

    @staticmethod
    def schema_config():
        return DatasetConfig


class DatasetConfig(BaseConfig):
    SCHEMA = DatasetSchema
    IDENTIFIER = 'dataset'

    def __init__(self, uuid, name, description, is_public):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.is_public = is_public
