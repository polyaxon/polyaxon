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


class MPIJobSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.MPIJOB))
    clean_pod_policy = fields.Str(
        allow_none=True, validate=validate.OneOf(V1CleanPodPolicy.allowable_values)
    )
    slots_per_worker = fields.Int(allow_none=True)
    launcher = fields.Nested(KFReplicaSchema, allow_none=True)
    worker = fields.Nested(KFReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1MPIJob


class V1MPIJob(BaseConfig, polyaxon_sdk.V1MPIJob):
    """Kubeflow MPI-Job provides an interface to train distributed experiments with Pytorch.

    Args:
        kind: str, should be equal `mpijob`
        clean_pod_policy: str, one of [`All`, `Running`, `None`]
        slots_per_worker: int, optional
        launcher: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional
        worker: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: mpijob
    >>>   cleanPodPolicy:
    >>>   slots_per_worker:
    >>>   launcher:
    >>>   worker:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1KFReplica, V1MPIJob
    >>> from polyaxon.k8s import k8s_schemas
    >>> mpi_job = V1MPIJob(
    >>>     clean_pod_policy='All',
    >>>     launcher=V1KFReplica(...),
    >>>     worker=V1KFReplica(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this
    component's runtime is a mpijob.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: mpijob
    ```

    ### cleanPodPolicy

    Controls the deletion of pods when a job terminates.
    The policy can be one of the following values: [`All`, `Running`, `None`]


    ```yaml
    >>> run:
    >>>   kind: mpijob
    >>>   cleanPodPolicy: 'All'
    >>>  ...
    ```

    ### launcher

    The launcher replica in the distributed mpijob

    ```yaml
    >>> run:
    >>>   kind: mpijob
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
    >>>   kind: mpijob
    >>>   worker:
    >>>     replicas: 3
    >>>     container:
    >>>       ...
    >>>  ...
    ```
    """

    SCHEMA = MPIJobSchema
    IDENTIFIER = V1RunKind.MPIJOB
    REDUCED_ATTRIBUTES = [
        "slotsPerWorker",
        "cleanPodPolicy",
        "launcher",
        "worker",
    ]
