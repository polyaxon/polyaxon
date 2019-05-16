# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import fields, ValidationError, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import IntOrStr, UUID


def validate_dep(**kwargs):
    if len([i for i in six.itervalues(kwargs) if i is not None]) != 1:
        raise ValidationError('One and only one value, [id, uuid, name], is allowed for declaring a dependency.')


class DepSchema(BaseSchema):
    id = IntOrStr(allow_none=True)
    uuid = UUID(allow_none=True)
    name = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return DepConfig

    @validates_schema
    def validate_dep(self, data):
        validate_dep(**data)


class DepConfig(BaseConfig):
    SCHEMA = DepSchema
    IDENTIFIER = 'dep'

    def __init__(self, id=None, uuid=None, name=None):  # pylint:disable=redefined-builtin
        validate_dep(id=id, uuid=uuid, name=name)
        self.id = id
        self.uuid = uuid
        self.name = name
