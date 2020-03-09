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
import random

import polyaxon_sdk

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.containers.names import INIT_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField
from polyaxon.schemas.types import (
    ArtifactsTypeSchema,
    DockerfileTypeSchema,
    GitTypeSchema,
)


class InitSchema(BaseCamelSchema):
    artifacts = fields.Nested(ArtifactsTypeSchema, allow_none=True)
    git = fields.Nested(GitTypeSchema, allow_none=True)
    dockerfile = fields.Nested(DockerfileTypeSchema, allow_none=True)
    connection = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": INIT_CONTAINER.format(random.randint(1, 100))},
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return V1Init

    @validates_schema
    def validate_init(self, data, **kwargs):
        artifacts = data.get("artifacts")
        git = data.get("git")
        dockerfile = data.get("dockerfile")
        connection = data.get("connection")
        schemas = 0
        if artifacts:
            schemas += 1
        if git:
            schemas += 1
        if dockerfile:
            schemas += 1
        if schemas > 1:
            raise ValidationError("One of artifacts, git, or dockerfile can be set")

        if not connection and git and not git.url:
            raise ValidationError(
                "git field without a valid url requires a connection is required to be passed."
            )


class V1Init(BaseConfig, polyaxon_sdk.V1Init):
    IDENTIFIER = "init"
    SCHEMA = InitSchema
    REDUCED_ATTRIBUTES = [
        "artifacts",
        "git",
        "dockerfile",
        "connection",
        "path",
        "container",
    ]

    def has_connection(self):
        return any([self.connection, self.git, self.dockerfile, self.artifacts])
