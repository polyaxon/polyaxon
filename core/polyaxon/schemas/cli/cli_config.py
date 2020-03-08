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

from polyaxon.schemas.api.log_handler import LogHandlerSchema
from polyaxon.schemas.base import BaseConfig, BaseSchema


class CliConfigurationSchema(BaseSchema):
    check_count = fields.Int(allow_none=True)
    current_version = fields.Str(allow_none=True)
    server_versions = fields.Dict(allow_none=True)
    log_handler = fields.Nested(LogHandlerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return CliConfigurationConfig


class CliConfigurationConfig(BaseConfig):
    SCHEMA = CliConfigurationSchema
    IDENTIFIER = "cli"
    MIN = "0.0.0"
    LATEST = "9.9.9"

    def __init__(
        self,
        check_count=0,
        current_version=None,
        server_versions=None,
        log_handler=None,
    ):
        self.check_count = check_count
        self.current_version = current_version
        self.server_versions = server_versions
        self.log_handler = log_handler

    @property
    def min_version(self):
        if not self.server_versions or "cli" not in self.server_versions:
            return self.MIN
        cli_version = self.server_versions["cli"] or {}
        return cli_version.get("min_version", self.MIN)

    @property
    def latest_version(self):
        if not self.server_versions or "cli" not in self.server_versions:
            return self.LATEST
        cli_version = self.server_versions["cli"] or {}
        return cli_version.get("latest_version", self.LATEST)
