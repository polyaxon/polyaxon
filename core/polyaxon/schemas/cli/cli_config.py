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
from polyaxon.schemas.cli.checks_config import ChecksConfig, ChecksSchema


class CliSchema(ChecksSchema):
    current_version = fields.Str(allow_none=True)
    installation = fields.Dict(allow_none=True)
    compatibility = fields.Dict(allow_none=True)
    log_handler = fields.Nested(LogHandlerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return CliConfig


class CliConfig(ChecksConfig):
    SCHEMA = CliSchema
    IDENTIFIER = "cli"
    INTERVAL = 30 * 60

    def __init__(
        self,
        current_version=None,
        installation=None,
        compatibility=None,
        log_handler=None,
        last_check=None,
    ):
        self.current_version = current_version
        self.installation = installation
        self.compatibility = compatibility
        self.log_handler = log_handler
        super().__init__(last_check=last_check)

    @property
    def min_version(self):
        if not self.compatibility or "cli" not in self.compatibility:
            return None
        cli_version = self.compatibility["cli"] or {}
        return cli_version.get("min")

    @property
    def latest_version(self):
        if not self.compatibility or "cli" not in self.compatibility:
            return None
        cli_version = self.compatibility["cli"] or {}
        return cli_version.get("latest")
