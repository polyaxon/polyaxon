#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from marshmallow import fields

import polyaxon_sdk

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class TensorboardTypeSchema(BaseCamelSchema):
    port = RefOrObject(fields.Int(allow_none=True))
    uuids = RefOrObject(fields.List(fields.Str(allow_none=True)))
    use_names = RefOrObject(fields.Bool(allow_none=True))
    path_prefix = RefOrObject(fields.Str(allow_none=True))
    plugins = RefOrObject(fields.List(fields.Str(allow_none=True)))

    @staticmethod
    def schema_config():
        return V1TensorboardType


class V1TensorboardType(BaseTypeConfig, polyaxon_sdk.V1TensorboardType):
    """Tensorboard type.

    This type allows to initialize Tensorboard logs foe one or multiple operations.

    Args:
        port: int
        uuids: List[str]
        use_names: bool, optional
        path_prefix: str, optional
        plugins: List[str]

    ### YAML usage

    ### Usage in IO and params definition

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: tensorboard_content
    >>>     type: tensorboard
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   tensorboard_content:
    >>>     value:
    >>>       port: 6006
    >>>       uuids: "d1410a914d18457589b91926d8c23db4,56f1a7f20f1d4f7f9e1a108b3c6b6031"
    >>>       useNames: true
    ```

    ### Usage in initializers

    ```yaml
     ```yaml
    >>> version:  1.1
    >>> kind: component
    >>> run:
    >>>   kind: service
    >>>   init:
    >>>   - tensorboard:
    >>>       uuids: "{{uuids}}"
    >>>       port: "{{globals.ports[0]}}"
    >>>       pathPrefix: "{{globals.base_url}}"
    >>>       useNames: true
    >>>       plugins: "tensorboard-plugin-profile"
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
    >>>         name="tensorboard_content",
    >>>         type=types.TENSORBOARD,
    >>>     ),
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>>
    >>> params = {
    >>>     "test1": V1Param(
    >>>         value=types.V1TensorboardType(
    >>>             port=6006,
    >>>             uuids="d1410a914d18457589b91926d8c23db4,56f1a7f20f1d4f7f9e1a108b3c6b6031",
    >>>             use_names=True,
    >>>         )
    >>>     ),
    >>> }
    ```

    ### Usage in initializers

    ```python
    >>> from polyaxon.polyflow import V1Component, V1Init, V1Job
    >>> from polyaxon.schemas.types import V1FileType
    >>> from polyaxon.k8s import k8s_schemas
    >>> component = V1Component(
    >>>     run=V1Job(
    >>>        init=[
    >>>             V1Init(
    >>>                 file=V1TensorboardType(
    >>>                     uuids="{{uuids}}",
    >>>                     port="{{globals.ports[0]}}",
    >>>                     path_prefix="{{globals.base_url}}",
    >>>                     use_names=True,
    >>>                     plugins="tensorboard-plugin-profile",
    >>>                 )
    >>>             ),
    >>>        ],
    >>>        container=k8s_schemas.V1Container(...)
    >>>     )
    >>> )
    ```

    ### Fields
      * port: port to expose the tensorboard service.
      * uuids: comma separated list of operation's uuids to load the tensorboard logs from.
      * useNames: an optional flag to initialize the paths under the operation's names.
      * pathPrefix: an optional path prefix to use for exposing the service.
      * plugins: an optional comma separated list of plugins to install before starting the tensorboard service.
    """

    IDENTIFIER = "tensorboard"
    SCHEMA = TensorboardTypeSchema
    REDUCED_ATTRIBUTES = [
        "port",
        "uuids",
        "useNames",
        "pathPrefix",
        "plugins",
    ]
