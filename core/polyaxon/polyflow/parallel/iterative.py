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

from marshmallow import fields, validate

from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.polyflow.parallel.matrix import MatrixSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.fields.swagger import SwaggerField


class IterativeSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("iterative"))
    num_iterations = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    concurrency = fields.Int(allow_none=True)
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": MAIN_JOB_CONTAINER},
        allow_none=True,
    )
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Iterative


class V1Iterative(BaseConfig, polyaxon_sdk.V1Iterative):
    IDENTIFIER = "iterative"
    SCHEMA = IterativeSchema
    REDUCED_ATTRIBUTES = ["params", "seed", "container", "earlyStopping", "concurrency"]
