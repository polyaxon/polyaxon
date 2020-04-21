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
import uuid

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyboard.artifacts.kinds import V1ArtifactKind
from polyaxon.schemas.base import BaseConfig, BaseSchema


class RunArtifactSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    kind = fields.Str(
        allow_none=True, validate=validate.OneOf(V1ArtifactKind.allowable_values)
    )
    path = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)
    summary = fields.Dict(allow_none=True)
    connection = fields.Str(allow_none=True)
    is_input = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1RunArtifact


class V1RunArtifact(BaseConfig, polyaxon_sdk.V1RunArtifact):
    IDENTIFIER = "artifact"
    SCHEMA = RunArtifactSchema
    REDUCED_ATTRIBUTES = [
        "name",
        "kind",
        "path",
        "state",
        "summary",
        "connection",
        "is_input",
    ]

    @classmethod
    def from_model(cls, model):
        return cls(
            name=model.name,
            kind=model.kind,
            path=model.path,
            state=model.state,
            summary=model.summary,
            # connection=model.connection,  # TODO: enable
        )

    def get_state(self, namespace: uuid.UUID):
        if self.state:
            return self.state

        if self.path:
            return uuid.uuid5(namespace, self.path)

        return uuid.uuid5(namespace, str(self.summary))
