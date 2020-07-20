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


class GitTypeSchema(BaseCamelSchema):
    url = RefOrObject(fields.Str(allow_none=True))
    revision = RefOrObject(fields.Str(allow_none=True))
    connection = RefOrObject(fields.Str(allow_none=True))
    init = RefOrObject(fields.Bool(allow_none=True))

    @staticmethod
    def schema_config():
        return V1GitType


class V1GitType(BaseTypeConfig, polyaxon_sdk.V1GitType):
    """Git type allows you to pass a git repo as a parameter.

    If used as an input type, Polyaxon can resolve several git connections
    and will turn this input type into an initializer with logic to clone
    the repo with support of branches and commits,
    the requested repo will be exposed as a context for your jobs and operations.

    Args:
        url: str, optional.
        revision: str, optional.
        connection: str, optional.
        init: bool, optioanl.

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: git
    >>>   - name: test2
    >>>     type: git
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1: {value: {"url": "https://github.com/tensorflow/models"}}
    >>>   test2: {value: {connection: "my-git-connection", revision: "branchA"}}
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
    >>>         iotype=types.GIT,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         iotype=types.GIT,
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
    >>>         value=types.V1GitType(url="https://github.com/tensorflow/models")
    >>>     ),
    >>>     "test2": V1Param(
    >>>         value=types.V1GitType(connection="my-git-connection", revision="branchA")
    >>>     ),
    >>> }
    ```
    """

    IDENTIFIER = "git"
    SCHEMA = GitTypeSchema
    REDUCED_ATTRIBUTES = ["url", "revision", "connection", "init"]

    def get_name(self):
        if self.url:
            return self.url.split("/")[-1].split(".")[0]
        return None
