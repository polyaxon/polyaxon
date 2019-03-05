# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class PersistenceSchema(BaseSchema):
    data = fields.List(fields.Str(), allow_none=True)
    outputs = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceConfig


class PersistenceConfig(BaseConfig):
    """
    Persistence config.

    Defines the list of persistent volumes to mount for this specific run.

    Args:
        data: `list(str)`. The list of the names of data persistence to mount.
        outputs: `list(str)`. The list of the names of outputs persistence to mount.
    """
    IDENTIFIER = 'persistence'
    SCHEMA = PersistenceSchema

    def __init__(self, data=None, outputs=None):
        self.data = data
        self.outputs = outputs
