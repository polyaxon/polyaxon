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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema
from polyaxon_sdk import V1GridSearch

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.schemas.polyflow.parallel.matrix import MatrixSchema


def validate_matrix(matrix):
    if not matrix:
        return None

    for key, value in six.iteritems(matrix):
        if value.is_distribution:
            raise ValidationError(
                "`{}` defines a distribution, "
                "and it cannot be used with grid search.".format(key)
            )

    return matrix


class GridSearchSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("grid_search"))
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), required=True
    )
    concurrency = fields.Int(allow_none=True)
    n_runs = RefOrObject(fields.Int(allow_none=True, validate=validate.Range(min=1)))
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return GridSearchConfig

    @validates_schema
    def validate_matrix(self, data):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get("matrix"))


class GridSearchConfig(BaseConfig, V1GridSearch):
    SCHEMA = GridSearchSchema
    IDENTIFIER = "grid_search"
    REDUCED_ATTRIBUTES = ["n_runs", "concurrency", "early_stopping"]
    IDENTIFIER_KIND = True
