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


class S3TypeSchema(BaseCamelSchema):
    bucket = RefOrObject(fields.Str(allow_none=True))
    key = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1S3Type


class V1S3Type(BaseTypeConfig, polyaxon_sdk.V1S3Type):
    """S3 type.

    Args:
        bucket: str
        key: str

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: s3
    >>>   - name: test2
    >>>     type: s3
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: {bucket: "s3://bucket1"}}
    >>>   test1: {value: {bucket: "s3://bucket2", key: "keyName"}}
    ```

    ### Python usage

    The inputs definition

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1IO
    >>> inputs = [
    >>>     V1IO(
    >>>         name="test1",
    >>>         iotype=types.S3,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         iotype=types.S3,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(value=types.V1S3Type(bucket="s3://bucket1")),
    >>>     "test2": V1Param(value=types.V1S3Type(bucket="s3://bucket1", key="keyName")),
    >>> }
    ```
    """

    IDENTIFIER = "s3"
    SCHEMA = S3TypeSchema
    REDUCED_ATTRIBUTES = ["bucket", "key"]

    def __str__(self):
        path = "s3://{}".format(self.bucket)
        if self.key:
            path = "{}/{}".format(path, self.key)
        return path

    def __repr__(self):
        return str(self)

    def to_param(self):
        return str(self)
