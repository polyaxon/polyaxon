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


class GitTypeSchema(BaseCamelSchema):
    url = RefOrObject(fields.Str(allow_none=True))
    revision = RefOrObject(fields.Str(allow_none=True))
    flags = RefOrObject(fields.List(fields.Str(), allow_none=True))

    @staticmethod
    def schema_config():
        return V1GitType


class V1GitType(BaseTypeConfig, polyaxon_sdk.V1GitType):
    """Git type allows you to pass a git repo as a parameter.

    If used as an input type, Polyaxon can resolve several git connections
    and will turn this input type into an initializer with logic to clone
    the repo with support for branches and commits,
    the requested repo will be exposed as a context for your jobs and operations.

    Args:
        url: str, optional.
        revision: str, optional.
        flags: List[str], optional

    ### YAML usage

    ### Usage in IO and params definition

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
    >>>   test2: {value: {revision: "branchA"}, connection: "my-git-connection"}
    >>>   test3: {
    >>>     value: {flags: ["--recursive", "-c http.sslVerify=false"]},
    >>>     connection: "my-git-connection",
    >>>   }
    ```

    ### Usage in initializers

    ```yaml
    >>> version:  1.1
    >>> kind: component
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>   - git: {"url": "https://github.com/tensorflow/models"}
    >>>   - git:
    >>>       revision: branchA
    >>>     connection: my-git-connection
    >>>   - git:
    >>>       flags: ["--recursive", "-c http.sslVerify=false"]
    >>>     connection: my-git-connection
    >>>   ...
    ```

    ### Python usage

    ### Usage in IO and params definition

    The inputs definition

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1IO
    >>> inputs = [
    >>>     V1IO(
    >>>         name="test1",
    >>>         type=types.GIT,
    >>>     ),
    >>>     V1IO(
    >>>         name="test2",
    >>>         type=types.GIT,
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
    >>>         value=types.V1GitType(revision="branchA"),
    >>>         connection="my-git-connection",
    >>>     ),
    >>> }
    ```

    ### Usage in initializers
    ```python
    >>> from polyaxon.polyflow import V1Component, V1Init, V1Job
    >>> from polyaxon.schemas.types import V1GitType
    >>> from polyaxon.k8s import k8s_schemas
    >>> component = V1Component(
    >>>     run=V1Job(
    >>>        init=[
    >>>             V1Init(
    >>>               git=V1GitType(url="https://github.com/tensorflow/models"),
    >>>             ),
    >>>             V1Init(
    >>>               git=V1GitType(revision="branchA"),
    >>>               connection="my-git-connection",
    >>>             ),
    >>>        ],
    >>>        container=k8s_schemas.V1Container(...)
    >>>     )
    >>> )
    ```
    """

    IDENTIFIER = "git"
    SCHEMA = GitTypeSchema
    REDUCED_ATTRIBUTES = ["url", "revision", "flags"]

    def get_name(self):
        if self.url:
            return self.url.split("/")[-1].split(".")[0]
        return None
