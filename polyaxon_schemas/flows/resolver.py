# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.base import BaseOneOfSchema
from polyaxon_schemas.registry import SchemaRegistry


class OpResolverSchema(BaseOneOfSchema):
    TYPE_FIELD = 'kind'
    TYPE_FIELD_remove = False
    SCHEMAS = SchemaRegistry(base_operations={}, polyflow_operations={})
