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


class ArtifactsTypeSchema(BaseCamelSchema):
    connection = RefOrObject(fields.Str(allow_none=True))
    files = RefOrObject(fields.List(fields.Str(), allow_none=True))
    dirs = RefOrObject(fields.List(fields.Str(), allow_none=True))
    init = RefOrObject(fields.Bool(allow_none=True))
    workers = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1ArtifactsType


class V1ArtifactsType(BaseConfig, polyaxon_sdk.V1ArtifactsType):
    """Artifacts type allows to easily pass
    the files and directories to initialize as a single parameter.

    If used as an input type, Polyaxon can resolve several connections (blob storage and volumes)
    and will turn this input type into an initializer with logic to download/provide
    the requested files and/or directories into a context for your jobs and operations.


    Args:
        connection: str, optional, the connection to use,
                    if not provided the default artifacts store is used
        files: List[str], optional, list of file subpaths
        dirs: List[str], optional, list of directory subpaths
        init: bool, optional, if True the files and the dirs will be automatically
              downloaded / provided in the run's artifacts context.
        workers: int, optional, number of threads for downloading data from S3/GCS/Azure.

    ### YAML usage

    The inputs definition

    ```yaml
    >>> inputs:
    >>>   - name: some-file-names
    >>>     type: artifacts
    >>>   - name: tensorboard-log-dir
    >>>     type: artifacts
    >>>   - name: dataset1
    >>>     type: artifacts
    ```

    The params usage

    ```yaml
    >>> params:
    >>>   some-file-names: {value: {files: ["file1", "/path/to/file2"]}}
    >>>   tensorboard-log-dir: {value: {dirs: ["/tensorboard-logs"], connection: "foo", init: True}}
    >>>   dataset1: {value: {connection: "s3-dataset", init: True}}
    ```

    The first param will be just a list of files definition that the user should know how to handle in their program.

    The second param, Polyaxon will load only that directory path from connection "foo".
    This connection could be any bycket or volume.

    In the third param, `dataset1` will be resolved automatically because
    Polyaxon knows about that connection and that it's of type S3.
    It will load all data in that S3 bucket before starting the experiment.

    ### Python usage

    The inputs definition

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1IO
    >>> inputs = [
    >>>     V1IO(
    >>>         name="some-file-names",
    >>>         iotype=types.ARTIFACTS,
    >>>     ),
    >>>     V1IO(
    >>>         name="tensorboard-log-dir",
    >>>         iotype=types.ARTIFACTS,
    >>>     ),
    >>>     V1IO(
    >>>         name="dataset1",
    >>>         iotype=types.ARTIFACTS,
    >>>     )
    >>> ]
    ```

    The params usage

    ```python
    >>> from polyaxon import types
    >>> from polyaxon.schemas import types
    >>> from polyaxon.polyflow import V1Param
    >>> params = {
    >>>     "test1": V1Param(value=types.V1ArtifactsType(files=["file1", "/path/to/file2"])),
    >>>     "test2": V1Param(
    >>>         value=types.V1ArtifactsType(dirs=["/tensorboard-logs"], connection="foo", init=True)
    >>>     ),
    >>>     "test3": V1Param(
    >>>         value=types.V1ArtifactsType(connection="s3-dataset", init=True, workers=10)
    >>>     ),
    >>> }
    ```
    """

    IDENTIFIER = "artifacts"
    SCHEMA = ArtifactsTypeSchema
    REDUCED_ATTRIBUTES = ["files", "dirs", "connection", "init", "workers"]
