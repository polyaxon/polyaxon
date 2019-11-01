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


class ServiceLevelSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    multiple = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return ServiceLevelConfig


class ServiceLevelConfig(BaseConfig):
    IDENTIFIER = "service_level"
    SCHEMA = ServiceLevelSchema
    REDUCED_ATTRIBUTES = ["enabled", "multiple"]

    def __init__(self, enabled=None, multiple=None):
        self.enabled = enabled
        self.multiple = multiple
