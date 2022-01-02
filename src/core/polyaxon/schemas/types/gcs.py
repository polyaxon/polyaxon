#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import os

import polyaxon_sdk

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class GcsTypeSchema(BaseCamelSchema):
    bucket = RefOrObject(fields.Str(allow_none=True))
    blob = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1GcsType


class V1GcsType(BaseTypeConfig, polyaxon_sdk.V1GcsType):
    """GCS type.

    Args:
        bucket: str
        blob: str

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: gcs
    >>>   - name: test2
    >>>     type: gcs
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: {bucket: "gs://bucket1"}}
    >>>   test1: {value: {bucket: "gs://bucket2", blob: "blobName"}}
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
    >>>         type=types.GCS,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         type=types.GCS,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(value=types.V1GcsType(bucket="gs://bucket1")),
    >>>     "test2": V1Param(value=types.V1GcsType(bucket="gs://bucket1", blob="blobName")),
    >>> }
    ```
    """

    IDENTIFIER = "gcs"
    SCHEMA = GcsTypeSchema
    REDUCED_ATTRIBUTES = ["bucket", "blob"]

    def __str__(self):
        path = "gs://{}".format(self.bucket)
        if self.blob:
            path = os.path.join(path, self.blob)
        return path

    def __repr__(self):
        return str(self)

    def to_param(self):
        return str(self)
