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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class UISchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    offline = fields.Bool(allow_none=True)
    static_url = fields.Str(allow_none=True)
    assets_version = fields.Str(allow_none=True)
    admin_enabled = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return UIConfig


class UIConfig(BaseConfig):
    SCHEMA = UISchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "jsOffline",
        "staticUrl",
        "assetsVersion",
        "adminEnabled",
    ]

    def __init__(
        self,
        enabled=None,
        offline=None,
        static_url=None,
        assets_version=None,
        admin_enabled=None,
    ):
        self.enabled = enabled
        self.offline = offline
        self.assets_version = assets_version
        self.static_url = static_url
        self.admin_enabled = admin_enabled
