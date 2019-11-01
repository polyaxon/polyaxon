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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.ops.container import ContainerSchema
from polyaxon.schemas.ops.environments import EnvironmentSchema
from polyaxon.schemas.ops.mounts import MountsSchema
from polyaxon.schemas.ops.termination import TerminationSchema


class OpReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    mounts = fields.Nested(MountsSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return OpReplicaConfig


class OpReplicaConfig(BaseConfig):
    SCHEMA = OpReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = ["replicas", "environment", "termination", "mounts"]

    def __init__(self, replicas=None, environment=None, termination=None, mounts=None):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.mounts = mounts


class JobReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    mounts = fields.Nested(MountsSchema, allow_none=True)
    container = fields.Nested(ContainerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return JobReplicaConfig


class JobReplicaConfig(BaseConfig):
    SCHEMA = JobReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = [
        "replicas",
        "environment",
        "termination",
        "mounts",
        "container",
    ]

    def __init__(
        self,
        replicas=None,
        environment=None,
        termination=None,
        mounts=None,
        container=None,
    ):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.mounts = mounts
        self.container = container
