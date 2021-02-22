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

from marshmallow import fields, validate

from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig


class FileTypeSchema(BaseCamelSchema):
    content = RefOrObject(fields.Str(), required=True)
    filename = RefOrObject(fields.Str(allow_none=True))
    kind = RefOrObject(
        fields.Str(
            allow_none=True, validate=validate.OneOf(V1ArtifactKind.allowable_values)
        )
    )
    chmod = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1FileType


class V1FileType(BaseTypeConfig, polyaxon_sdk.V1FileType):
    """File type.

    This type allows you to easily construct pass a file content without
    the need to clone repo or download a from an external localtion.
    It exposes a very simple interface for generating a file or a script
    that can be used by your containers.

    Args:
        content: str
        filename: str, optional
        kind: str, optional
        chmod: str, optional

    ### YAML usage

    ### Usage in IO and params definition

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: file
    >>>   - name: test2
    >>>     type: file
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1:
    >>>     value:
    >>>       filename: script.sh
    >>>       chmod: +x
    >>>       content: |
    >>>         #!/usr/bin/env bash
    >>>
    >>>         echo 'This is a test.' | wc -w
    >>>   test2:
    >>>     value:
    >>>       filename: script.py
    >>>       content: |
    >>>         print("hello world")
    >>>
    ```

    ### Usage in initializers

    ```yaml
     ```yaml
    >>> version:  1.1
    >>> kind: component
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>   - file:
    >>>       filename: script.sh
    >>>       chmod: +x
    >>>       content: |
    >>>         #!/usr/bin/env bash
    >>>
    >>>         echo 'This is a test.' | wc -w
    >>>   - file:
    >>>       filename: script.py
    >>>       content: |
    >>>         print("hello world")
    >>>     ...
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
    >>>         type=types.FILE,
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
    >>>         value=types.V1FileType(
    >>>             filename="script.sh",
    >>>             chmod="+x",
    >>>             content="#!/usr/bin/env bash\necho 'This is a test.' | wc -w",
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
    >>>                 file=V1FileType(
    >>>                     filename="script.sh",
    >>>                     chmod="+x",
    >>>                     content="#!/usr/bin/env bash\necho 'This is a test.' | wc -w",
    >>>                 )
    >>>             ),
    >>>        ],
    >>>        container=k8s_schemas.V1Container(...)
    >>>     )
    >>> )
    ```

    ### Fields
      * filename: an optional filename.
      * content: the content of the file or script.
      * chmod: Custom permission for the generated file.
      * kind: artifact kind, default to `file`.
    """

    IDENTIFIER = "file"
    SCHEMA = FileTypeSchema
    REDUCED_ATTRIBUTES = [
        "filename",
        "kind",
        "content",
        "chmod",
    ]
