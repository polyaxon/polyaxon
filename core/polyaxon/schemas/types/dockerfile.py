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

from marshmallow import fields, validates_schema

from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.fields.docker_image import validate_image
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.types.base import BaseTypeConfig
from polyaxon.utils.signal_decorators import check_partial

POLYAXON_DOCKERFILE_NAME = "Dockerfile"
POLYAXON_DOCKER_WORKDIR = "/code"
POLYAXON_DOCKER_SHELL = "/bin/bash"


class DockerfileTypeSchema(BaseCamelSchema):
    image = RefOrObject(fields.Str(), required=True)
    env = RefOrObject(fields.Dict(keys=fields.Str(), allow_none=True))
    path = RefOrObject(fields.List(fields.Str(), allow_none=True))
    copy = RefOrObject(fields.List(fields.Str(), allow_none=True))
    run = RefOrObject(fields.List(fields.Str(), allow_none=True))
    lang_env = RefOrObject(fields.Str(allow_none=True))
    uid = RefOrObject(fields.Int(allow_none=True))
    gid = RefOrObject(fields.Int(allow_none=True))
    filename = RefOrObject(fields.Str(allow_none=True))
    workdir = RefOrObject(fields.Str(allow_none=True))
    workdir_path = RefOrObject(fields.Str(allow_none=True))
    shell = RefOrObject(fields.Str(allow_none=True))

    @staticmethod
    def schema_config():
        return V1DockerfileType

    @validates_schema
    @check_partial
    def validate_dockerfile(self, data, **kwargs):
        validate_image(data.get("image"))


class V1DockerfileType(BaseTypeConfig, polyaxon_sdk.V1DockerfileType):
    """Dockerfile type.

    This type allows you to easily construct a dockerfile without
    the need to clone repo or download a file. It exposes a very simple interface for generating
    a dockerfile to build your container.

    Args:
        image: str
        env: Dict, optional
        path: List[str], optional
        copy: List[str], optional
        run: List[str], optional
        lang_env: str, optional
        uid: str, optional
        gid: str, optional
        filename: str, optional
        workdir: str, optional
        workdir_path: str, optional
        shell: str, optional

    ### YAML usage

    ### Usage in IO and params definition

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: test1
    >>>     type: dockerfile
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   test1:
    >>>     value:
    >>>       image: test
    >>>       run: ["pip install package1"]
    >>>       env: {'KEY1': 'en_US.UTF-8', 'KEY2':2}
    ```

    ### Usage in initializers

    ```yaml
     ```yaml
    >>> version:  1.1
    >>> kind: component
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>   - dockerfile:
    >>>       image: test
    >>>       run: ["pip install package1"]
    >>>       env: {'KEY1': 'en_US.UTF-8', 'KEY2':2}
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
    >>>         type=types.DOCKERFILE,
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
    >>>         value=types.V1DockerfileType(
    >>>             image="test:version",
    >>>             run=["pip install package1"],
    >>>             env={'KEY1': 'en_US.UTF-8', 'KEY2':2}
    >>>         )
    >>>     ),
    >>> }
    ```

    ### Usage in initializers

    ```python
    >>> from polyaxon.polyflow import V1Component, V1Init, V1Job
    >>> from polyaxon.schemas.types import V1DockerfileType
    >>> from polyaxon.k8s import k8s_schemas
    >>> component = V1Component(
    >>>     run=V1Job(
    >>>        init=[
    >>>             V1Init(
    >>>                 dockerfile=V1DockerfileType(
    >>>                     image="test",
    >>>                     run=["pip install package1"],
    >>>                     env={'KEY1': 'en_US.UTF-8', 'KEY2':2},
    >>>                 )
    >>>             ),
    >>>        ],
    >>>        container=k8s_schemas.V1Container(...)
    >>>     )
    >>> )
    ```

    ### Fields
      * image: the base image to use, is will exposed as `FROM` command in the dockerfile.
      * env: environment variables dictionary that will be exposed as `ENV` sections.
      * path: list of paths to be added to your `PATH` environment variable.
      * copy: a list a copy commands that will be exposed as list of COPY commands.
      * run: a list a run commands that will be exposed as list of RUN commands.
      * langEnv: if passed it will expose these environment variable: ENV LC_ALL, LANG, LANGUAGE
      * uid and gid: will create a new user based on these 2 values.
      * filename: an optional name for your dockerfile, default is Dockerfile.
        **N.B.** this is not a path, if you need to generate the dockerfile on a custom path,
        you will need to set the path key on the init container definition.
      * workdir: the WORKDIR for your dockerfile, default is `/code`
      * workdirPath: the local workdir to copy to the docker container.
      * shell: shell type environment variable, default `/bin/bash`.

    ### Example

    ```yaml
    >>> image: image:tag
    >>> env:
    >>>   KEY1: value1
    >>>   KEY2: value2
    >>> path:
    >>> - module/add/to/path
    >>> copy:
    >>> - copy/local/path
    >>> run:
    >>> - pip install ...
    >>> - mv foo bar
    >>> langEnv: en_US.UTF-8
    >>> uid: 2222
    >>> gid: 1111
    >>> filename: Dockerfile2
    >>> workdir: ../my-code
    ```
    """

    IDENTIFIER = "dockerfile"
    SCHEMA = DockerfileTypeSchema
    REDUCED_ATTRIBUTES = [
        "image",
        "env",
        "path",
        "copy",
        "run",
        "langEnv",
        "uid",
        "gid",
        "filename",
        "workdir",
        "workdirPath",
        "shell",
    ]

    @property
    def filename(self):
        return (
            self._filename if self._filename is not None else POLYAXON_DOCKERFILE_NAME
        )

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def workdir(self):
        return self._workdir if self._workdir is not None else POLYAXON_DOCKER_WORKDIR

    @workdir.setter
    def workdir(self, workdir):
        self._workdir = workdir

    @property
    def shell(self):
        return self._shell if self._shell is not None else POLYAXON_DOCKER_SHELL

    @shell.setter
    def shell(self, shell):
        self._shell = shell

    @property
    def image_tag(self):
        if not self.image:
            return None
        tagged_image = self.image.split(":")
        if len(tagged_image) == 1:
            return "latest"
        if len(tagged_image) == 2:
            return "latest" if "/" in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
