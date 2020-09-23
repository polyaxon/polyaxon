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


class ArtifactsTypeSchema(BaseCamelSchema):
    files = RefOrObject(fields.List(fields.Str(), allow_none=True))
    dirs = RefOrObject(fields.List(fields.Str(), allow_none=True))
    workers = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1ArtifactsType


class V1ArtifactsType(BaseTypeConfig, polyaxon_sdk.V1ArtifactsType):
    """Artifacts type allows to easily pass
    the files and directories to initialize as a single parameter.

    If used as an input type, Polyaxon can resolve several connections (blob storage and volumes)
    and will turn this input type into an initializer with logic to download/provide
    the requested files and/or directories into a context for your jobs and operations.


    Args:
        files: List[str], optional, list of file subpaths
        dirs: List[str], optional, list of directory subpaths
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
    >>>   tensorboard-log-dir: {value: {dirs: ["/tensorboard-logs"]}, connection: "foo", toInit: True}
    >>>   dataset1: {value: {value: {dirs: ["/"]}, connection: "s3-dataset", init: True}
    ```

    The first param will be just a list of files definition that
    the user should know how to handle in their program.

    The second param, Polyaxon will load only that directory path from connection "foo".
    This connection could be any a bucket or a volume.

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
    >>>         value=types.V1ArtifactsType(dirs=["/tensorboard-logs"]),
    >>>         connection="foo",
    >>>         to_init=True
    >>>     ),
    >>>     "test3": V1Param(
    >>>         value=types.V1ArtifactsType(dirs=["/"], workers=10),
    >>>         connection="s3-dataset",
    >>>         to_init=True
    >>>     ),
    >>> }
    ```
    """

    IDENTIFIER = "artifacts"
    SCHEMA = ArtifactsTypeSchema
    REDUCED_ATTRIBUTES = ["files", "dirs", "workers"]
