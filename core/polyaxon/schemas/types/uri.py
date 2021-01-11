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

import polyaxon_sdk

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class UriTypeSchema(BaseCamelSchema):
    user = RefOrObject(fields.Str(required=True))
    password = RefOrObject(fields.Str(required=True))
    host = RefOrObject(fields.Str(required=True))

    @staticmethod
    def schema_config():
        return V1UriType


class V1UriType(BaseTypeConfig, polyaxon_sdk.V1UriType):
    """Uri type.

    Args:
        user: str
        password: str
        host: str

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: uri
    >>>   - name: test2
    >>>     type: uri
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: "username1:password1@service.com"}
    >>>   test1: {value: {"user": "username2", "password": "password2", "host": "service.com"}
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
    >>>         iotype=types.URI,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(
    >>>         value=types.V1AuthType(user="username1", password="password1", host="service.com")
    >>>     ),
    >>> }
    ```

    > Normally you should not be passing auth details in plain values.
    """

    IDENTIFIER = "uri"
    SCHEMA = UriTypeSchema
    REDUCED_ATTRIBUTES = ["user", "password", "host"]

    def __str__(self):
        return "{}:{}@{}".format(self.user, self.password, self.host)

    def __repr__(self):
        return str(self)

    def to_param(self):
        return str(self)
