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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class ImageSchema(BaseCamelSchema):
    name = RefOrObject(fields.Str(allow_none=True))
    connection = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1ImageType


class V1ImageType(BaseTypeConfig, polyaxon_sdk.V1ImageType):
    IDENTIFIER = "image"
    SCHEMA = ImageSchema
    REDUCED_ATTRIBUTES = ["name", "connection"]
