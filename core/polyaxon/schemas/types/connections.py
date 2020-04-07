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
from typing import Optional

import polyaxon_sdk

from marshmallow import fields, pre_load, validate

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    ConnectionSchema,
    K8sResourceSchema,
    V1BucketConnection,
    V1ClaimConnection,
    V1GitConnection,
    V1HostConnection,
    V1HostPathConnection,
)
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.types.k8s_resources import V1K8sResourceType


class ConnectionTypeSchema(BaseCamelSchema):
    name = fields.Str(required=True)
    kind = fields.Str(required=True, validate=validate.OneOf(V1ConnectionKind.VALUES))
    schema = fields.Nested(ConnectionSchema, allow_none=True)
    secret = fields.Nested(K8sResourceSchema, allow_none=True)
    config_map = fields.Nested(K8sResourceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1ConnectionType

    @pre_load
    def pre_make(self, data, **kwargs):
        schema = data.get("schema")
        kind = data.get("kind")
        if schema and kind:
            if kind in V1ConnectionKind.BLOB_VALUES:
                schema["kind"] = V1BucketConnection.IDENTIFIER

            if kind == V1ConnectionKind.VOLUME_CLAIM:
                schema["kind"] = V1ClaimConnection.IDENTIFIER

            if kind == V1ConnectionKind.HOST_PATH:
                schema["kind"] = V1HostPathConnection.IDENTIFIER

            if kind == V1ConnectionKind.REGISTRY:
                schema["kind"] = V1HostConnection.IDENTIFIER

            if kind == V1ConnectionKind.GIT:
                schema["kind"] = V1GitConnection.IDENTIFIER

        return data


class V1ConnectionType(BaseConfig, polyaxon_sdk.V1ConnectionType):
    IDENTIFIER = "connection"
    SCHEMA = ConnectionTypeSchema
    REDUCED_ATTRIBUTES = ["name", "kind", "schema", "secret", "configMap"]

    @classmethod
    def from_model(cls, model) -> "V1ConnectionType":
        schema = model.schema
        secret = model.secret
        config_map = model.config_map
        if hasattr(schema, "to_dict"):
            schema = schema.to_dict()
        if hasattr(secret, "to_dict"):
            secret = secret.to_dict()
        if hasattr(config_map, "to_dict"):
            config_map = config_map.to_dict()
        return V1ConnectionType.from_dict(
            {
                "name": model.name,
                "kind": model.kind,
                "schema": schema,
                "secret": secret,
                "configMap": config_map,
            }
        )

    @property
    def store_path(self) -> str:
        if self.is_mount:
            return self.schema.mount_path
        if self.is_bucket:
            return self.schema.bucket

    @property
    def is_mount(self) -> bool:
        return V1ConnectionKind.is_mount(self.kind)

    @property
    def is_artifact(self) -> bool:
        return V1ConnectionKind.is_artifact(self.kind)

    @property
    def is_host_path(self) -> bool:
        return V1ConnectionKind.is_host_path(self.kind)

    @property
    def is_volume_claim(self) -> bool:
        return V1ConnectionKind.is_volume_claim(self.kind)

    @property
    def is_bucket(self) -> bool:
        return V1ConnectionKind.is_bucket(self.kind)

    @property
    def is_gcs(self) -> bool:
        return self.kind == V1ConnectionKind.GCS

    @property
    def is_s3(self) -> bool:
        return self.kind == V1ConnectionKind.S3

    @property
    def is_wasb(self) -> bool:
        return V1ConnectionKind.is_wasb(self.kind)

    def get_secret(self) -> Optional[V1K8sResourceType]:
        if self.secret:
            return V1K8sResourceType(name=self.secret.name, schema=self.secret)
        return None

    def get_config_map(self) -> Optional[V1K8sResourceType]:
        if self.config_map:
            return V1K8sResourceType(name=self.config_map.name, schema=self.config_map)
        return None
