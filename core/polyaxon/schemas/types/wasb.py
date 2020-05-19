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

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class WasbTypeSchema(BaseCamelSchema):
    container = RefOrObject(fields.Str(allow_none=True))
    storage_account = RefOrObject(fields.Str(allow_none=True))
    path = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1WasbType


class V1WasbType(BaseConfig, polyaxon_sdk.V1WasbType):
    """Wasb type.

    Args:
        container: str
        storage_account: str
        path: str

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: wasb
    >>>   - name: test2
    >>>     type: wasb
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: {container: "containerName", user: "username"}}
    >>>   test2: {value: {container: "containerName", user: "username", key: "some/path"}}
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
    >>>         iotype=types.WASB,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         iotype=types.WASB,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(value=types.V1WasbType(container="containerName", user="username")),
    >>>     "test2": V1Param(
    >>>         value=types.V1WasbType(
    >>>              container="containerName2", user="username", path="path/value"
    >>>         )
    >>>      ),
    >>> }
    ```
    """

    IDENTIFIER = "wasb"
    SCHEMA = WasbTypeSchema
    REDUCED_ATTRIBUTES = ["container", "storageAccount", "path"]
