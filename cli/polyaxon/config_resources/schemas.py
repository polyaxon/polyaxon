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

from marshmallow import ValidationError, fields

from polyaxon.config_resources.kinds import ConfigResourceKind
from polyaxon_sdk import V1ConfigResourceSchema

from polyaxon.schemas.base import BaseConfig, BaseSchema


class ConfigResourceSchema(BaseSchema):
    ref = fields.Str(required=True)
    mount_path = fields.Str(allow_none=True)
    items = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return ConfigResourceConfig


class ConfigResourceConfig(BaseConfig, V1ConfigResourceSchema):
    SCHEMA = ConfigResourceSchema
    IDENTIFIER = "config_resource"


def validate_config_resource(kind, definition):
    if kind not in ConfigResourceKind.VALUES:
        raise ValidationError("Connection with kind {} is not supported.".format(kind))

    ConfigResourceConfig.from_dict(definition)
