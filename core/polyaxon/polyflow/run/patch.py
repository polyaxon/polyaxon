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


from typing import Dict

from marshmallow import ValidationError

from polyaxon.polyflow.run.dag import V1Dag
from polyaxon.polyflow.run.dask import V1Dask
from polyaxon.polyflow.run.job import V1Job
from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.polyflow.run.kubeflow.mpi_job import V1MPIJob
from polyaxon.polyflow.run.kubeflow.pytorch_job import V1PytorchJob
from polyaxon.polyflow.run.kubeflow.replica import V1KFReplica
from polyaxon.polyflow.run.kubeflow.tf_job import V1TFJob
from polyaxon.polyflow.run.notifier import V1Notifier
from polyaxon.polyflow.run.service import V1Service
from polyaxon.polyflow.run.spark.replica import V1SparkReplica
from polyaxon.polyflow.run.spark.spark import V1Spark
from polyaxon.polyflow.run.tuner import V1Tuner


def validate_run_patch(run_patch: Dict, kind: V1RunKind.allowable_values):
    if kind == V1RunKind.JOB:
        patch = V1Job.from_dict(run_patch)
    elif kind == V1RunKind.SERVICE:
        patch = V1Service.from_dict(run_patch)
    elif kind == V1RunKind.DAG:
        patch = V1Dag.from_dict(run_patch)
    elif kind == V1RunKind.MPIJOB:
        try:
            patch = V1MPIJob.from_dict(run_patch)
        except ValidationError:
            patch = V1KFReplica.from_dict(run_patch)
    elif kind == V1RunKind.PYTORCHJOB:
        try:
            patch = V1PytorchJob.from_dict(run_patch)
        except ValidationError:
            patch = V1KFReplica.from_dict(run_patch)
    elif kind == V1RunKind.TFJOB:
        try:
            patch = V1TFJob.from_dict(run_patch)
        except ValidationError:
            patch = V1KFReplica.from_dict(run_patch)
    elif kind == V1RunKind.SPARK:
        try:
            patch = V1Spark.from_dict(run_patch)
        except ValidationError:
            patch = V1SparkReplica.from_dict(run_patch)
    elif kind == V1RunKind.DASK:
        patch = V1Dask.from_dict(run_patch)
    elif kind == V1RunKind.NOTIFIER:
        patch = V1Notifier.from_dict(run_patch)
    elif kind == V1RunKind.TUNER:
        patch = V1Tuner.from_dict(run_patch)
    else:
        raise ValidationError("runPatch cannot be validate without a supported kind.")

    return patch
