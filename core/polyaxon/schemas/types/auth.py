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


class AuthTypeSchema(BaseCamelSchema):
    user = RefOrObject(fields.Str(), required=True)
    password = RefOrObject(fields.Str(), required=True)

    @staticmethod
    def schema_config():
        return V1AuthType


class V1AuthType(BaseTypeConfig, polyaxon_sdk.V1AuthType):
    """Auth type.

    Args:
        user: str
        password: str

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: auth
    >>>   - name: test2
    >>>     type: auth
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: "username1:password1"}
    >>>   test1: {value: {"user": "username2", "password": "password2"}}
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
    >>>         iotype=types.AUTH,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         iotype=types.AUTH,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(value=types.V1AuthType(user="username1", password="password1")),
    >>>     "test2": V1Param(value=types.V1AuthType(user="username2", password="password2")),
    >>> }
    ```

    > Normally you should not be passing auth details in plain values.

    This type validate several values:

    String values:
       * '{"user": "foo", "password": "bar"}'
       * 'foo:bar'

    Dict values:
       * {"user": "foo", "password": "bar"}
    """

    IDENTIFIER = "auth"
    SCHEMA = AuthTypeSchema
    REDUCED_ATTRIBUTES = ["user", "password"]

    def __str__(self):
        return "{}:{}".format(self.user, self.password)

    def __repr__(self):
        return str(self)
