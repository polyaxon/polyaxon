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

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.polyflow.run.replica import ReplicaSchema


class MpiJobSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("mpi_job"))
    slots_per_worker = fields.Int(allow_none=True)
    launcher = fields.Nested(ReplicaSchema, allow_none=True)
    worker = fields.Nested(ReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return MpiJobConfig


class MpiJobConfig(BaseConfig):
    SCHEMA = MpiJobSchema
    IDENTIFIER = "mpi_job"
    REDUCED_ATTRIBUTES = ["slots_per_worker", "launcher", "worker"]

    def __init__(
        self, slots_per_worker=None, launcher=None, worker=None, kind=IDENTIFIER
    ):
        self.kind = kind
        self.launcher = launcher
        self.worker = worker
        self.slots_per_worker = slots_per_worker
