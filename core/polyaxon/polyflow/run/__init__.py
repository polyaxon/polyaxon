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

from polyaxon.polyflow.run.job import V1Job, JobSchema
from polyaxon.polyflow.run.notifier import V1Notifier, NotifierSchema
from polyaxon.polyflow.run.ray import RaySchema, V1Ray
from polyaxon.polyflow.run.service import ServiceSchema, V1Service
from polyaxon.schemas.base import BaseOneOfSchema
from polyaxon.polyflow.run.dag import V1Dag, DagSchema
from polyaxon.polyflow.run.dask import V1Dask, DaskSchema
from polyaxon.polyflow.run.flink import V1Flink, FlinkSchema
from polyaxon.polyflow.run.kubeflow.replica import KFReplicaSchema, V1KFReplica
from polyaxon.polyflow.run.kubeflow.mpi_job import V1MPIJob, MPIJobSchema
from polyaxon.polyflow.run.kubeflow.clean_pod_policy import V1CleanPodPolicy
from polyaxon.polyflow.run.kubeflow.pytorch_job import V1PytorchJob, PytorchJobSchema
from polyaxon.polyflow.run.kubeflow.tf_job import V1TFJob, TFJobSchema
from polyaxon.polyflow.run.spark.replica import V1SparkReplica, SparkReplicaSchema
from polyaxon.polyflow.run.spark.spark import (
    V1Spark,
    SparkSchema,
    V1SparkType,
    V1SparkDeploy,
)
from polyaxon.polyflow.run.kinds import V1RunKind, V1CloningKind, V1PipelineKind


class RunSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1RunKind.JOB: JobSchema,
        V1RunKind.SERVICE: ServiceSchema,
        V1RunKind.DAG: DagSchema,
        V1RunKind.MPIJOB: MPIJobSchema,
        V1RunKind.PYTORCHJOB: PytorchJobSchema,
        V1RunKind.TFJOB: TFJobSchema,
        V1RunKind.SPARK: SparkSchema,
        V1RunKind.FLINK: FlinkSchema,
        V1RunKind.DASK: DaskSchema,
        V1RunKind.RAY: RaySchema,
        V1RunKind.NOTIFIER: NotifierSchema,
    }


class RunMixin(object):
    def get_run_kind(self):
        raise NotImplementedError

    @property
    def is_job_run(self):
        return self.get_run_kind() == V1RunKind.JOB

    @property
    def is_service_run(self):
        return self.get_run_kind() == V1RunKind.SERVICE

    @property
    def is_mpi_job_run(self):
        return self.get_run_kind() == V1RunKind.MPIJOB

    @property
    def is_pytorch_job_run(self):
        return self.get_run_kind() == V1RunKind.PYTORCHJOB

    @property
    def is_tf_job_run(self):
        return self.get_run_kind() == V1RunKind.TFJOB

    @property
    def is_spark_run(self):
        return self.get_run_kind() == V1RunKind.SPARK

    @property
    def is_flink_run(self):
        return self.get_run_kind() == V1RunKind.FLINK

    @property
    def is_dask_run(self):
        return self.get_run_kind() == V1RunKind.DASK

    @property
    def is_dag_run(self):
        return self.get_run_kind() == V1RunKind.DAG

    @property
    def is_notifier(self):
        return self.get_run_kind() == V1RunKind.NOTIFIER

    @property
    def is_distributed_run(self):
        return self.is_mpi_job_run or self.is_pytorch_job_run or self.is_tf_job_run
