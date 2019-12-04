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
from polyaxon.schemas.polyflow.init.build_context import BuildContextSchema
from polyaxon.schemas.polyflow.init.repo_init import RepoInitSchema
from polyaxon.schemas.polyflow.mounts import ArtifactMountSchema
from polyaxon_sdk import V1Init


class InitSchema(BaseSchema):
    repos = fields.Nested(RepoInitSchema, many=True, allow_none=True)
    artifacts = fields.Nested(ArtifactMountSchema, many=True, allow_none=True)
    build = fields.Nested(BuildContextSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return InitConfig


class InitConfig(BaseConfig, V1Init):
    """
    Init config.
    """

    IDENTIFIER = "init"
    SCHEMA = InitSchema
    REDUCED_ATTRIBUTES = ["repos", "artifacts", "build"]
