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
from polyaxon_sdk import V1TFJob

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.polyflow.run.replica import ReplicaSchema


class TFJobSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("tfjob"))
    chief = fields.Nested(ReplicaSchema, allow_none=True)
    ps = fields.Nested(ReplicaSchema, allow_none=True)
    worker = fields.Nested(ReplicaSchema, allow_none=True)
    evaluator = fields.Nested(ReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return TFJobConfig


class TFJobConfig(BaseConfig, V1TFJob):
    SCHEMA = TFJobSchema
    IDENTIFIER = "tfjob"
    REDUCED_ATTRIBUTES = ["chief", "ps", "worker", "evaluator"]
    IDENTIFIER_KIND = True
