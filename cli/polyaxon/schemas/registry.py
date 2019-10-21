#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from copy import copy

from hestia.imports import import_string

from polyaxon.exceptions import PolyaxonConfigurationError
from polyaxon.schemas.ops.operation import BaseOpSchema


class SchemaRegistry(object):
    def __init__(self, base_operations, polyflow_operations):
        self.base_operations = base_operations
        self.polyflow_operations = self._setup_polyflow(polyflow_operations)
        self._schemas = self._setup(
            base_operations=base_operations, polyflow_operations=polyflow_operations
        )

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
                    "Schema {} at path: {} is not a valid operation.".format(
                        schema_name, schema_path
                    )
                )
            ops[schema_name] = schema

        return ops
