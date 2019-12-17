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
from polyaxon_sdk import (
    V1BlobConnection,
    V1ClaimConnection,
    V1HostConnection,
    V1HostPathConnection,
)

from polyaxon.connections.kinds import ConnectionKind
from polyaxon.schemas.base import BaseConfig, BaseSchema


class BlobConnectionSchema(BaseSchema):
    blob = fields.Str(required=True)

    @staticmethod
    def schema_config():
        return BlobConnectionConfig


class BlobConnectionConfig(BaseConfig, V1BlobConnection):
    SCHEMA = BlobConnectionSchema
    IDENTIFIER = "blob"


class ClaimConnectionSchema(BaseSchema):
    volume_claim = fields.Str(required=True)
    mount_path = fields.Str(required=True)
    read_only = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return ClaimConnectionConfig


class ClaimConnectionConfig(BaseConfig, V1ClaimConnection):
    SCHEMA = ClaimConnectionSchema
    IDENTIFIER = "claim"


class HostPathConnectionSchema(BaseSchema):
    host_path = fields.Str(required=True)
    mount_path = fields.Str(required=True)
    read_only = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return HostPathConnectionConfig


class HostPathConnectionConfig(BaseConfig, V1HostPathConnection):
    SCHEMA = HostPathConnectionSchema
    IDENTIFIER = "host_path"


class HostConnectionSchema(BaseSchema):
    url = fields.Str(required=True)
    insecure = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return HostConnectionConfig


class HostConnectionConfig(BaseConfig, V1HostConnection):
    SCHEMA = HostConnectionSchema
    IDENTIFIER = "host"


def validate_connection(kind, definition):
    if kind not in ConnectionKind.VALUES:
        raise ValidationError("Connection with kind {} is not supported.".format(kind))

    if kind in ConnectionKind.BLOB_VALUES:
        BlobConnectionConfig.from_dict(definition)

    if kind == ConnectionKind.VOLUME_CLAIM:
        ClaimConnectionConfig.from_dict(definition)

    if kind == ConnectionKind.HOST_PATH:
        HostPathConnectionConfig.from_dict(definition)

    if kind in {ConnectionKind.GIT, ConnectionKind.REGISTRY}:
        HostPathConnectionConfig.from_dict(definition)
