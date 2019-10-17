# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

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
