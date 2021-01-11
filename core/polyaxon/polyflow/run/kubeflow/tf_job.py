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

from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.polyflow.run.kubeflow.clean_pod_policy import V1CleanPodPolicy
from polyaxon.polyflow.run.kubeflow.replica import KFReplicaSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class TFJobSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.TFJOB))
    clean_pod_policy = fields.Str(
        allow_none=True, validate=validate.OneOf(V1CleanPodPolicy.allowable_values)
    )
    chief = fields.Nested(KFReplicaSchema, allow_none=True)
    ps = fields.Nested(KFReplicaSchema, allow_none=True)
    worker = fields.Nested(KFReplicaSchema, allow_none=True)
    evaluator = fields.Nested(KFReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1TFJob


class V1TFJob(BaseConfig, polyaxon_sdk.V1TFJob):
    """Kubeflow TF-Job provides an interface to train distributed experiments with TensorFlow.

    Args:
        kind: str, should be equal `tfjob`
        clean_pod_policy: str, one of [`All`, `Running`, `None`]
        chief: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional
        ps: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional
        worker: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional
        evaluator: [V1KFReplica](/docs/experimentation/distributed/kubeflow-replica/), optional

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   cleanPodPolicy:
    >>>   chief:
    >>>   ps:
    >>>   worker:
    >>>   evaluator:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1KFReplica, V1TFJob
    >>> from polyaxon.k8s import k8s_schemas
    >>> tf_job = V1TFJob(
    >>>     clean_pod_policy='All',
    >>>     chief=V1KFReplica(...),
    >>>     ps=V1KFReplica(...),
    >>>     worker=V1KFReplica(...),
    >>>     evaluator=V1KFReplica(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this component's runtime is a tfjob.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: tfjob
    ```

    ### cleanPodPolicy

    Controls the deletion of pods when a job terminates.
    The policy can be one of the following values: [`All`, `Running`, `None`]


    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   cleanPodPolicy: 'All'
    >>>  ...
    ```

    ### chief

    The chief is responsible for orchestrating training and performing
    tasks like checkpointing the model.

    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   chief:
    >>>     replicas: 1
    >>>     container:
    >>>       ...
    >>>  ...
    ```

    ### ps

    The ps are parameter servers; these servers provide a distributed data store
    for the model parameters.

    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   ps:
    >>>     replicas: 2
    >>>     container:
    >>>       ...
    >>>  ...
    ```

    ### worker

    The workers do the actual work of training the model. In some cases,
    worker 0 might also act as the chief.

    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   worker:
    >>>     replicas: 2
    >>>     container:
    >>>       ...
    >>>  ...
    ```

    ### evaluator

    The evaluators can be used to compute evaluation metrics as the model is trained.

    ```yaml
    >>> run:
    >>>   kind: tfjob
    >>>   evaluator:
    >>>     replicas: 1
    >>>     container:
    >>>       ...
    >>>  ...
    ```
    """

    SCHEMA = TFJobSchema
    IDENTIFIER = V1RunKind.TFJOB
    REDUCED_ATTRIBUTES = [
        "cleanPodPolicy",
        "chief",
        "ps",
        "worker",
        "evaluator",
    ]
