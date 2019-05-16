# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from copy import copy

from hestia.imports import import_string

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.operation import BaseOpSchema


class SchemaRegistry(object):
    def __init__(self, base_operations, polyflow_operations):
        self.base_operations = base_operations
        self.polyflow_operations = self._setup_polyflow(polyflow_operations)
        self._schemas = self._setup(base_operations=base_operations,
                                    polyflow_operations=polyflow_operations)

    def _setup(self, base_operations, polyflow_operations):
        schemas = copy(base_operations)
        schemas.update(polyflow_operations)
        return schemas

    def _setup_polyflow(self, polyflow_operations):
        if not polyflow_operations:
            return {}
        ops = {}
        for schema_name, schema_path in polyflow_operations:
            schema = import_string(schema_path)
            if not issubclass(schema, BaseOpSchema):
                raise PolyaxonConfigurationError(
                    'Schema {} at path: {} is not a valid operation.'.format(
                        schema_name, schema_path))
            ops[schema_name] = schema

        return ops
