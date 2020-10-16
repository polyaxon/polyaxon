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

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.containers.names import POLYAXON_INIT_PREFIX, generate_container_name
from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField
from polyaxon.schemas.types import (
    ArtifactsTypeSchema,
    DockerfileTypeSchema,
    GitTypeSchema,
)


class InitSchema(BaseCamelSchema):
    artifacts = fields.Nested(ArtifactsTypeSchema, allow_none=True)
    git = fields.Nested(GitTypeSchema, allow_none=True)
    dockerfile = fields.Nested(DockerfileTypeSchema, allow_none=True)
    connection = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": generate_container_name(prefix=POLYAXON_INIT_PREFIX)},
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return V1Init

    @validates_schema
    def validate_init(self, data, **kwargs):
        artifacts = data.get("artifacts")
        git = data.get("git")
        dockerfile = data.get("dockerfile")
        connection = data.get("connection")
        schemas = 0
        if artifacts:
            schemas += 1
        if git:
            schemas += 1
        if dockerfile:
            schemas += 1
        if schemas > 1:
            raise ValidationError("One of artifacts, git, or dockerfile can be set")

        if not connection and git and not git.url:
            raise ValidationError(
                "git field without a valid url requires a connection is required to be passed."
            )


class V1Init(BaseConfig, polyaxon_sdk.V1Init):
    """Polyaxon init section exposes an interface for users to run init
    containers before the main container containing the logic for training models
    or processing data.

    Polyaxon init section is an extension of
    [Kubernetes init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).  # noqa

    Polyaxon init section has special handlers for several connections in addition to the possibility for the users to
    provide their own containers and run any custom init containers which can contain utilities
    or setup scripts not present in the main container.

    By default, all built-in handlers will mount and initialize data under the path
    `/plx-context/artifacts/{{connection-name}}` unless the user passes a custom `path`.

    Args:
        artifacts: [V1ArtifactsType](/docs/core/specification/types/#v1artifactstype), optional
        git: [V1GitType](/docs/core/specification/types/#v1gittype), optional
        dockerfile: [V1DockerfileType](/docs/core/specification/types/#v1dockerfiletype), optional
        connection: str, optional
        path: str, optional
        container: [Kubernetes Container](https://kubernetes.io/docs/concepts/containers/), optional


    ## YAML usage

    You can only use one of the possibilities for built-in handlers,
    otherwise an exception will be raised.
    It's possible to customize the container used with the default built-in handlers.

    ```yaml
    >>> version:  1.1
    >>> kind: component
    >>> run:
    >>>   kind: job
    >>>   init:
    >>>   - artifacts:
    >>>       dirs: ["path/on/the/default/artifacts/store"]
    >>>   - connection: gcs-large-datasets
    >>>     artifacts:
    >>>       dirs: ["data"]
    >>>     container:
    >>>       resources:
    >>>         requests:
    >>>           memory: "256Mi"
    >>>           cpu: "500m"
    >>>   - connection: s3-datasets
    >>>     path: "/s3-path"
    >>>     artifacts:
    >>>       files: ["data1", "path/to/data2"]
    >>>   - connection: repo1
    >>>   - git:
    >>>       revision: branch2
    >>>     connection: repo2
    >>>   - dockerfile:
    >>>       image: test
    >>>       run: ["pip install package1"]
    >>>       env: {'KEY1': 'en_US.UTF-8', 'KEY2':2}
    >>>   - container:
    >>>       name: myapp-container
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo custom init container']
    >>>
    >>>   container:
    >>>     ...
    ```

    ## Python usage

    Similar to the YAML example if you pass more than one handler, an exception will be raised.
    It's possible to customize the container used with the default built-in handlers.

    ```python
    >>> from polyaxon.polyflow import V1Component, V1Init, V1Job
    >>> from polyaxon.schemas.types import V1ArtifactsType, V1DockerfileType, V1GitType
    >>> from polyaxon.k8s import k8s_schemas
    >>> component = V1Component(
    >>>     run=V1Job(
    >>>        init=[
    >>>             V1Init(
    >>>                 artifacts=V1ArtifactsType(dirs=["path/on/the/default/artifacts/store"])
    >>>             ),
    >>>             V1Init(
    >>>                 connection="gcs-large-datasets",
    >>>                 artifacts=V1ArtifactsType(dirs=["data"]),
    >>>                 container=k8s_schemas.V1Container(
    >>>                     resources=k8s_schemas.V1ResourceRequirements(requests={"memory": "256Mi", "cpu": "500m"}), # noqa
    >>>                 )
    >>>             ),
    >>>             V1Init(
    >>>               path="/s3-path",
    >>>               connection="s3-datasets",
    >>>                 artifacts=V1ArtifactsType(files=["data1", "path/to/data2"])
    >>>             ),
    >>>             V1Init(
    >>>               connection="repo1",
    >>>             ),
    >>>             V1Init(
    >>>               connection="repo2",
    >>>               git=V1GitType(revision="branch2")
    >>>             ),
    >>>             V1Init(
    >>>                 dockerfile=V1DockerfileType(
    >>>                     image="test",
    >>>                     run=["pip install package1"],
    >>>                     env={'KEY1': 'en_US.UTF-8', 'KEY2':2},
    >>>                 )
    >>>             ),
    >>>             V1Init(
    >>>                 container=k8s_schemas.V1Container(
    >>>                     name="myapp-container",
    >>>                     image="busybox:1.28",
    >>>                     command=['sh', '-c', 'echo custom init container']
    >>>                 )
    >>>             ),
    >>>        ],
    >>>        container=k8s_schemas.V1Container(...)
    >>>     )
    >>> )
    ```

    ## Understanding init section

    In both the YAML and Python example we are telling Polyaxon to initialize:
     * A directory `path/on/the/default/artifacts/store` from the default `artfactsStore`,
       because we did not specify a connection and we invoked an artifacts handler.
     * A directory `data` from a GCS connection named `gcs-large-datasets`, we also
       customized the built-in init container with a new resources section.
     * Two files `data1`, `path/to/data2` from an S3 connection named `s3-datasets`,
        and we specified that the 2 files should be initialized under
        `/s3-path` instead of the default path that Polyaxon uses.
     * A repo configured under the connection name `repo1` will be cloned from the default branch.
     * A repo configured under the connection name `repo2` will be cloned
        from the branch name `branch2`.
     * A dockerfile will be generated with the specification that was provided.
     * A custom container will finally run our own custom code, in this case an echo command.
    """

    IDENTIFIER = "init"
    SCHEMA = InitSchema
    REDUCED_ATTRIBUTES = [
        "artifacts",
        "git",
        "dockerfile",
        "connection",
        "path",
        "container",
    ]

    def has_connection(self):
        return any([self.connection, self.git, self.dockerfile, self.artifacts])
