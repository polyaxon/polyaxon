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

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.docker_image import validate_image
from polyaxon.schemas.fields.ref_or_obj import RefOrObject

POLYAXON_DOCKERFILE_NAME = "Dockerfile"
POLYAXON_DOCKER_WORKDIR = "/code"
POLYAXON_DOCKER_SHELL = "/bin/bash"


def validate_build_image(image):
    if not image:
        raise ValidationError(
            "Invalid Build context, an image or path to dockerfile is required."
        )
    validate_image(image)


class BuildContextSchema(BaseSchema):
    image = RefOrObject(fields.Str())
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
    name = RefOrObject(fields.Str(allow_none=True))
    workdir = RefOrObject(fields.Str(allow_none=True))
    code_path = RefOrObject(fields.Str(allow_none=True))
    shell = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return BuildContextConfig

    @validates_schema
    def validate(self, data):
        validate_build_image(data.get("image"))


class BuildContextConfig(BaseConfig):
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
        "name",
        "workdir",
        "code_path",
        "shell",
    ]

    def __init__(
        self,
        image=None,
        env=None,
        path=None,
        copy=None,
        run=None,
        lang_env=None,
        uid=None,
        gid=None,
        name=POLYAXON_DOCKERFILE_NAME,
        workdir=POLYAXON_DOCKER_WORKDIR,
        code_path=None,
        shell=POLYAXON_DOCKER_SHELL,
    ):
        validate_build_image(image)
        self.image = image
        self.env = env
        self.path = path
        self.run = run
        self.copy = copy
        self.lang_env = lang_env
        self.uid = uid
        self.gid = gid
        self.name = name
        self.workdir = workdir
        self.code_path = code_path
        self.shell = shell

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
