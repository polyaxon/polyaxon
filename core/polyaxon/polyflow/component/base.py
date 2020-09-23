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

from marshmallow import fields, validate

from polyaxon.polyflow.actions import ActionSchema
from polyaxon.polyflow.cache import CacheSchema
from polyaxon.polyflow.hooks import HookSchema
from polyaxon.polyflow.plugins import PluginsSchema
from polyaxon.polyflow.termination import TerminationSchema
from polyaxon.schemas.base import NAME_REGEX, BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class BaseComponentSchema(BaseCamelSchema):
    version = fields.Float(allow_none=True)
    kind = fields.Str(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    presets = fields.List(fields.Str(allow_none=True))
    queue = RefOrObject(fields.Str(allow_none=True))
    cache = fields.Nested(CacheSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    plugins = fields.Nested(PluginsSchema, allow_none=True)
    actions = fields.List(fields.Nested(ActionSchema), allow_none=True)
    hooks = fields.List(fields.Nested(HookSchema), allow_none=True)

    @staticmethod
    def schema_config():
        return BaseComponent


class BaseComponent(BaseConfig):
    SCHEMA = BaseComponentSchema
    REDUCED_ATTRIBUTES = [
        "version",
        "kind",
        "name",
        "description",
        "tags",
        "presets",
        "queue",
        "cache",
        "termination",
        "plugins",
        "actions",
        "hooks",
    ]
