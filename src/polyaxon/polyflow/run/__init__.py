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
from polyaxon.polyflow.run.cleaner import CleanerJobSchema, V1CleanerJob
from polyaxon.polyflow.run.dag import DagSchema, V1Dag
from polyaxon.polyflow.run.dask import DaskSchema, V1Dask
from polyaxon.polyflow.run.flink import FlinkSchema, V1Flink
from polyaxon.polyflow.run.job import JobSchema, V1Job
from polyaxon.polyflow.run.kinds import (
    V1CloningKind,
    V1PipelineKind,
    V1RunEdgeKind,
    V1RunKind,
)
from polyaxon.polyflow.run.kubeflow.clean_pod_policy import V1CleanPodPolicy
from polyaxon.polyflow.run.kubeflow.mpi_job import (
    MPIJobImplementation,
    MPIJobSchema,
    V1MPIJob,
)
from polyaxon.polyflow.run.kubeflow.mx_job import MXJobMode, MXJobSchema, V1MXJob
from polyaxon.polyflow.run.kubeflow.pytorch_job import PytorchJobSchema, V1PytorchJob
from polyaxon.polyflow.run.kubeflow.replica import KFReplicaSchema, V1KFReplica
from polyaxon.polyflow.run.kubeflow.scheduling_policy import V1SchedulingPolicy
from polyaxon.polyflow.run.kubeflow.tf_job import TFJobSchema, V1TFJob
from polyaxon.polyflow.run.kubeflow.xgboost_job import V1XGBoostJob, XGBoostJobSchema
from polyaxon.polyflow.run.notifier import NotifierJobSchema, V1NotifierJob
from polyaxon.polyflow.run.patch import validate_run_patch
from polyaxon.polyflow.run.ray import RaySchema, V1Ray
from polyaxon.polyflow.run.resources import V1RunResources
from polyaxon.polyflow.run.service import ServiceSchema, V1Service
from polyaxon.polyflow.run.spark.replica import SparkReplicaSchema, V1SparkReplica
from polyaxon.polyflow.run.spark.spark import (
    SparkSchema,
    V1Spark,
    V1SparkDeploy,
    V1SparkType,
)
from polyaxon.polyflow.run.tuner import TunerJobSchema, V1TunerJob
from polyaxon.schemas.base import BaseOneOfSchema


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
        V1RunKind.MXJOB: MXJobSchema,
        V1RunKind.XGBJOB: XGBoostJobSchema,
        V1RunKind.SPARK: SparkSchema,
        V1RunKind.FLINK: FlinkSchema,
        V1RunKind.DASK: DaskSchema,
        V1RunKind.RAY: RaySchema,
        V1RunKind.NOTIFIER: NotifierJobSchema,
        V1RunKind.CLEANER: CleanerJobSchema,
        V1RunKind.TUNER: TunerJobSchema,
    }


class RunMixin:
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
    def is_mx_job_run(self):
        return self.get_run_kind() == V1RunKind.MXJOB

    @property
    def is_xgb_job_run(self):
        return self.get_run_kind() == V1RunKind.XGBJOB

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
    def is_schedule_run(self):
        return self.get_run_kind() == V1RunKind.SCHEDULE

    @property
    def is_notifier_run(self):
        return self.get_run_kind() == V1RunKind.NOTIFIER

    @property
    def is_cleaner_run(self):
        return self.get_run_kind() == V1RunKind.CLEANER

    @property
    def is_tuner_run(self):
        return self.get_run_kind() == V1RunKind.TUNER

    @property
    def is_watchdog(self):
        return self.get_run_kind() == V1RunKind.WATCHDOG

    @property
    def is_distributed_run(self):
        return (
            self.is_mpi_job_run
            or self.is_pytorch_job_run
            or self.is_tf_job_run
            or self.is_mx_job_run
            or self.is_xgb_job_run
        )
