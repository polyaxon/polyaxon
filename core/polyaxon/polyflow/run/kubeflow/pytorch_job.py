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

from marshmallow import fields, validate

from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.polyflow.run.kubeflow.clean_pod_policy import V1CleanPodPolicy
from polyaxon.polyflow.run.kubeflow.replica import KFReplicaSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class PytorchJobSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.PYTORCHJOB))
    clean_pod_policy = fields.Str(
        allow_none=True, validate=validate.OneOf(V1CleanPodPolicy.allowable_values)
    )
    master = fields.Nested(KFReplicaSchema, allow_none=True)
    worker = fields.Nested(KFReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1PytorchJob


class V1PytorchJob(BaseConfig, polyaxon_sdk.V1PytorchJob):
    """Kubeflow Pytorch-Job provides an interface to train a distributed experiments with Pytorch.

    Args:
        kind: str, should be equal `pytorchjob`
        clean_pod_policy: str, one of [`All`, `Running`, `None`]
        master: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional
        worker: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: pytorchjob
    >>>   cleanPodPolicy:
    >>>   master:
    >>>   worker:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1KFReplica, V1PytorchJob
    >>> from polyaxon.k8s import k8s_schemas
    >>> pytorch_job = V1PytorchJob(
    >>>     clean_pod_policy='All',
    >>>     master=V1KFReplica(...),
    >>>     worker=V1KFReplica(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this
    component's runtime is a pytorchjob.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: pytorchjob
    ```

    ### cleanPodPolicy

    Controls deletion of pods when a job terminates.
    The policy can be one of the following values: [`All`, `Running`, `None`]


    ```yaml
    >>> run:
    >>>   kind: pytorchjob
    >>>   cleanPodPolicy: 'All'
    >>>  ...
    ```

    ### master

    The master replica in the distributed PytorchJob

    ```yaml
    >>> run:
    >>>   kind: pytorchjob
    >>>   master:
    >>>     replicas: 1
    >>>     container:
    >>>       ...
    >>>  ...
    ```

    ### worker

    The workers do the actual work of training the model.

    ```yaml
    >>> run:
    >>>   kind: pytorchjob
    >>>   worker:
    >>>     replicas: 3
    >>>     container:
    >>>       ...
    >>>  ...
    ```
    """

    SCHEMA = PytorchJobSchema
    IDENTIFIER = V1RunKind.PYTORCHJOB
    REDUCED_ATTRIBUTES = ["cleanPodPolicy", "master", "worker"]
