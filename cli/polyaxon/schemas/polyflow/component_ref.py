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

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.schemas.base import BaseConfig, BaseSchema


def validate_component_ref(**kwargs):
    if len([i for i in six.itervalues(kwargs) if i is not None and i != ""]) != 1:
        raise ValidationError(
            "Template requires one and only one param: " "name, url, path, or hub."
        )


class ComponentRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    hub = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return ComponentRefConfig

    @validates_schema
    def validate_component_ref(self, values):
        validate_component_ref(
            name=values.get("name"),
            url=values.get("url"),
            path=values.get("path"),
            hub=values.get("hub"),
        )


class ComponentRefConfig(BaseConfig):
    SCHEMA = ComponentRefSchema
    IDENTIFIER = "component_ref"
    REDUCED_ATTRIBUTES = ["name", "url", "path", "hub"]

    def __init__(self, name=None, url=None, path=None, hub=None):
        validate_component_ref(name=name, url=url, path=path, hub=hub)
        self.name = name
        self.url = url
        self.path = path
        self.hub = hub
