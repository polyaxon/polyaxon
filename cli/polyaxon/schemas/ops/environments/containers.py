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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class ContainerSchema(BaseSchema):
    image = fields.Str(allow_none=True)
    image_pull_policy = fields.Str(allow_none=True)
    sync_interval = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerConfig


class ContainerConfig(BaseConfig):
    SCHEMA = ContainerSchema
    IDENTIFIER = "container"
    REDUCED_ATTRIBUTES = ["image", "image_pull_policy", "sync_interval"]

    def __init__(self, image, image_pull_policy=None, sync_interval=None):
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.sync_interval = sync_interval
