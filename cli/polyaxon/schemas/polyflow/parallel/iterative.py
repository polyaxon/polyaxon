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

from marshmallow import fields, validate
from polyaxon_sdk import V1Iterative

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.schemas.polyflow.parallel.matrix import MatrixSchema
from polyaxon.schemas.polyflow.run.container import ContainerSchema


class IterativeSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("iterative"))
    n_iterations = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    concurrency = fields.Int(allow_none=True)
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    seed = RefOrObject(fields.Int(allow_none=True))
    container = fields.Nested(ContainerSchema, allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return IterativeConfig


class IterativeConfig(BaseConfig, V1Iterative):
    IDENTIFIER = "iterative"
    SCHEMA = IterativeSchema
    REDUCED_ATTRIBUTES = [
        "matrix",
        "seed",
        "container",
        "early_stopping",
        "concurrency",
    ]
    IDENTIFIER_KIND = True
