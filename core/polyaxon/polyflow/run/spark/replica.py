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

from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.environment import EnvironmentSchema
from polyaxon.polyflow.init import InitSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class SparkReplicaSchema(BaseCamelSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    init = fields.List(fields.Nested(InitSchema), allow_none=True)
    sidecars = fields.List(SwaggerField(cls=k8s_schemas.V1Container), allow_none=True)
    container = SwaggerField(
        cls=k8s_schemas.V1Container,
        defaults={"name": MAIN_JOB_CONTAINER},
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return V1SparkReplica


class V1SparkReplica(BaseConfig, polyaxon_sdk.V1SparkReplica):
    """Spark replica is the specification for a Spark executor or driver.

    Args:
        replicas: str, int
        environment: [V1Environment](/docs/core/specification/environment/), optional
        init: List[[V1Init](/docs/core/specification/init/)], optional
        sidecars: List[[sidecar containers](/docs/core/specification/sidecars/)],
                  optional
        container: [Kubernetes Container](https://kubernetes.io/docs/concepts/containers/)

    ## YAML usage

    ```yaml
    >>> executor/driver:
    >>>   replicas
    >>>   environment:
    >>>   init:
    >>>   sidecars:
    >>>   container:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Environment, V1Init, V1SparkReplica
    >>> from polyaxon.k8s import k8s_schemas
    >>> replica = V1SparkReplica(
    >>>     replicas=2,
    >>>     environment=V1Environment(...),
    >>>     init=[V1Init(...)],
    >>>     sidecars=[k8s_schemas.V1Container(...)],
    >>>     container=k8s_schemas.V1Container(...),
    >>> )
    ```

    ## Fields

    ### replicas

    The number of replica (executor/driver) instances.

    ```yaml
    >>> executor:
    >>>   replicas: 2
    ```

    ### environment

    Optional [environment section](/docs/core/specification/environment/),
    it provides a way to inject pod related information into the replica (executor/driver).

    ```yaml
    >>> driver:
    >>>   environment:
    >>>     labels:
    >>>        key1: "label1"
    >>>        key2: "label2"
    >>>      annotations:
    >>>        key1: "value1"
    >>>        key2: "value2"
    >>>      nodeSelector:
    >>>        node_label: node_value
    >>>      ...
    >>>  ...
    ```

    ### init

    A list of [init handlers and containers](/docs/core/specification/init/)
    to resolve for the replica (executor/driver).

    <blockquote class="light">
    If you are referencing a connection it must be configured.
    All referenced connections will be checked:

     * If they are accessible in the context of the project of this run

     * If the user running the operation can have access to those connections
    </blockquote>

    ```yaml
    >>> executor:
    >>>   init:
    >>>     - artifacts:
    >>>         dirs: ["path/on/the/default/artifacts/store"]
    >>>     - connection: gcs-large-datasets
    >>>       artifacts:
    >>>         dirs: ["data"]
    >>>       container:
    >>>         resources:
    >>>           requests:
    >>>             memory: "256Mi"
    >>>             cpu: "500m"
    >>>     - container:
    >>>       name: myapp-container
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo custom init container']
    ```

    ### sidecars


    A list of [sidecar containers](/docs/core/specification/sidecars/)
    that will used as sidecars.

    ```yaml
    >>> driver:
    >>>   sidecars:
    >>>     - name: sidecar2
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo sidecar2']
    >>>     - name: sidecar1
    >>>       image: busybox:1.28
    >>>       command: ['sh', '-c', 'echo sidecar1']
    >>>       resources:
    >>>         requests:
    >>>           memory: "128Mi"
    >>>           cpu: "500m"
    ```

    ### container

    The [main Kubernetes Container](https://kubernetes.io/docs/concepts/containers/)
    that will run your experiment training or data processing
    logic for the replica (executor/driver).

    ```yaml
    >>> executor:
    >>>   kind: job
    >>>   container:
    >>>     name: tensorflow:2.1
    >>>     init:
    >>>       - connection: my-tf-code-repo
    >>>     command: ["python", "/plx-context/artifacts/my-tf-code-repo/model.py"]
    ```
    """

    SCHEMA = SparkReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = [
        "replicas",
        "environment",
        "init",
        "sidecars",
        "container",
    ]
