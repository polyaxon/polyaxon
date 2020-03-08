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

import polyaxon_sdk

from marshmallow import fields, validates_schema

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.docker_image import validate_image
from polyaxon.schemas.fields.ref_or_obj import RefOrObject

POLYAXON_DOCKERFILE_NAME = "Dockerfile"
POLYAXON_DOCKER_WORKDIR = "/code"
POLYAXON_DOCKER_SHELL = "/bin/bash"


class DockerfileTypeSchema(BaseCamelSchema):
    image = RefOrObject(fields.Str(), required=True)
    env = RefOrObject(fields.Dict(keys=fields.Str(), allow_none=True))
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
        return V1DockerfileType

    @validates_schema
    def validate_dockerfile(self, data, **kwargs):
        validate_image(data.get("image"))


class V1DockerfileType(BaseConfig, polyaxon_sdk.V1DockerfileType):
    IDENTIFIER = "dockerfile"
    SCHEMA = DockerfileTypeSchema
    REDUCED_ATTRIBUTES = [
        "image",
        "env",
        "path",
        "copy",
        "run",
        "langEnv",
        "uid",
        "gid",
        "filename",
        "workdir",
        "workdirPath",
        "shell",
    ]

    @property
    def filename(self):
        return (
            self._filename if self._filename is not None else POLYAXON_DOCKERFILE_NAME
        )

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def workdir(self):
        return self._workdir if self._workdir is not None else POLYAXON_DOCKER_WORKDIR

    @workdir.setter
    def workdir(self, workdir):
        self._workdir = workdir

    @property
    def shell(self):
        return self._shell if self._shell is not None else POLYAXON_DOCKER_SHELL

    @shell.setter
    def shell(self, shell):
        self._shell = shell

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
