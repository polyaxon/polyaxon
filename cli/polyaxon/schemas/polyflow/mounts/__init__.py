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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.polyflow.mounts.artifact_mounts import ArtifactMountSchema
from polyaxon.schemas.polyflow.mounts.k8s_mounts import K8sMountSchema


class MountsSchema(BaseSchema):
    secrets = fields.Nested(K8sMountSchema, many=True, allow_none=True)
    config_maps = fields.Nested(K8sMountSchema, many=True, allow_none=True)
    artifacts = fields.Nested(ArtifactMountSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return MountsConfig


class MountsConfig(BaseConfig):
    """
    Mounts config.
    """

    IDENTIFIER = "mounts"
    SCHEMA = MountsSchema
    REDUCED_ATTRIBUTES = ["secrets", "config_maps", "artifacts"]

    def __init__(self, secrets=None, config_maps=None, artifacts=None):
        self.secrets = secrets
        self.config_maps = config_maps
        self.artifacts = artifacts
