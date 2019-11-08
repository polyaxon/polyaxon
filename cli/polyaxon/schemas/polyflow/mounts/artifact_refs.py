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
import warnings

from marshmallow import ValidationError, fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class ArtifactRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    paths = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return ArtifactRefConfig


class ArtifactRefConfig(BaseConfig):
    IDENTIFIER = "artifact_ref"
    SCHEMA = ArtifactRefSchema
    REDUCED_ATTRIBUTES = ["name", "paths"]

    def __init__(self, name, paths=None):
        self.name = name
        self.paths = paths


def validate_artifact_ref(values, field):
    field_value = values.get(field)
    if not field_value:
        return values
    field_value = [
        {"name": v} if isinstance(v, six.string_types) else v for v in field_value
    ]
    for v in field_value:
        try:
            ArtifactRefSchema(unknown=BaseConfig.UNKNOWN_BEHAVIOUR).load(v)
        except ValidationError:
            raise ValidationError("Persistence field `{}` is not value.".format(v))
    values[field] = field_value
    return values


def validate_artifact_refs(values):
    return validate_artifact_ref(values, "artifact_refs")


def validate_outputs(values):
    outputs = values.pop("outputs", None)
    if outputs:
        warnings.warn(
            "The `outputs` parameter is deprecated and will be removed in next release, "
            "please notice that it will be ignored.",
            DeprecationWarning,
        )
