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
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class K8sMountSchema(BaseSchema):
    name = fields.Str(required=True)
    mount_path = fields.Str(allow_none=True)
    items = RefOrObject(fields.List(fields.Str(), allow_none=True))

    @staticmethod
    def schema_config():
        return K8sMountConfig


class K8sMountConfig(BaseConfig):
    IDENTIFIER = "k8s_mount"
    SCHEMA = K8sMountSchema
    REDUCED_ATTRIBUTES = ["name", "mount_path", "items"]

    def __init__(self, name=None, mount_path=None, items=None):
        self.name = name
        self.mount_path = mount_path
        self.items = items
