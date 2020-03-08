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

from polyaxon.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class MappingSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("mapping"))
    values = RefOrObject(fields.List(fields.Dict(), required=True), required=True)
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Mapping


class V1Mapping(BaseConfig, polyaxon_sdk.V1Mapping):
    SCHEMA = MappingSchema
    IDENTIFIER = "mapping"
    REDUCED_ATTRIBUTES = ["concurrency", "earlyStopping"]
