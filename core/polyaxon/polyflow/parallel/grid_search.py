#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import polyaxon_sdk

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.parallel.matrix import MatrixSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


def validate_matrix(matrix):
    if not matrix:
        return None

    for key, value in matrix.items():
        if value.is_distribution:
            raise ValidationError(
                "`{}` defines a distribution, "
                "and it cannot be used with grid search.".format(key)
            )

    return matrix


class GridSearchSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("grid"))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), required=True
    )
    concurrency = fields.Int(allow_none=True)
    num_runs = RefOrObject(fields.Int(allow_none=True, validate=validate.Range(min=1)))
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1GridSearch

    @validates_schema
    def validate_matrix(self, data, **kwargs):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get("params"))


class V1GridSearch(BaseConfig, polyaxon_sdk.V1GridSearch):
    SCHEMA = GridSearchSchema
    IDENTIFIER = "grid"
    REDUCED_ATTRIBUTES = ["numRuns", "concurrency", "earlyStopping"]
