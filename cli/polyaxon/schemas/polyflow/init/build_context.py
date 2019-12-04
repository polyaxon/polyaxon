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

from marshmallow import fields, validate, validates_schema
from polyaxon_sdk import V1BuildContext

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.docker_image import validate_image
from polyaxon.schemas.fields.ref_or_obj import RefOrObject

POLYAXON_DOCKERFILE_NAME = "Dockerfile"
POLYAXON_DOCKER_WORKDIR = "/code"
POLYAXON_DOCKER_SHELL = "/bin/bash"


class BuildContextSchema(BaseSchema):
    image = RefOrObject(fields.Str(), required=True)
    env = RefOrObject(
        fields.List(
            fields.List(fields.Raw(), validate=validate.Length(equal=2)),
            allow_none=True,
        )
    )
    path = RefOrObject(fields.List(fields.Str(), allow_none=True))
    copy = RefOrObject(fields.List(fields.Str(), allow_none=True))
    run = RefOrObject(fields.List(fields.Str(), allow_none=True))
    lang_env = RefOrObject(fields.Str(allow_none=True))
    uid = RefOrObject(fields.Int(allow_none=True))
    gid = RefOrObject(fields.Int(allow_none=True))
    filename = RefOrObject(fields.Str(allow_none=True))
    workdir = RefOrObject(fields.Str(allow_none=True))
    workdir_path = RefOrObject(fields.Str(allow_none=True))
    shell = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return BuildContextConfig

    @validates_schema
    def validate(self, data):
        validate_image(data.get("image"))


class BuildContextConfig(BaseConfig, V1BuildContext):
    IDENTIFIER = "build_context"
    SCHEMA = BuildContextSchema
    REDUCED_ATTRIBUTES = [
        "image",
        "env",
        "path",
        "copy",
        "run",
        "lang_env",
        "uid",
        "gid",
        "filename",
        "workdir",
        "workdir_path",
        "shell",
    ]

    @property
    def filename(self):
        return self._filename or POLYAXON_DOCKERFILE_NAME

    @property
    def workdir(self):
        return self._workdir or POLYAXON_DOCKER_WORKDIR

    @property
    def shell(self):
        return self._shell or POLYAXON_DOCKER_SHELL

    @property
    def image_tag(self):
        if not self.image:
            return None
        tagged_image = self.image.split(":")
        if len(tagged_image) == 1:
            return "latest"
        if len(tagged_image) == 2:
            return "latest" if "/" in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
