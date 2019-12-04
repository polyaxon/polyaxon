#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from polyaxon.schemas.base import BaseOneOfSchema
from polyaxon.schemas.polyflow.run.container import ContainerConfig, ContainerSchema
from polyaxon.schemas.polyflow.run.dag import DagConfig, DagSchema
from polyaxon.schemas.polyflow.run.dask import DaskConfig, DaskSchema
from polyaxon.schemas.polyflow.run.flink import FlinkConfig, FlinkSchema
from polyaxon.schemas.polyflow.run.kubeflow.mpi_job import MpiJobConfig, MpiJobSchema
from polyaxon.schemas.polyflow.run.kubeflow.pytorch_job import (
    PytorchJobConfig,
    PytorchJobSchema,
)
from polyaxon.schemas.polyflow.run.kubeflow.tf_job import TFJobConfig, TFJobSchema
from polyaxon.schemas.polyflow.run.spark import SparkConfig, SparkSchema


class RunSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        DagConfig.IDENTIFIER: DagSchema,
        MpiJobConfig.IDENTIFIER: MpiJobSchema,
        PytorchJobConfig.IDENTIFIER: PytorchJobSchema,
        TFJobConfig.IDENTIFIER: TFJobSchema,
        SparkConfig.IDENTIFIER: SparkSchema,
        FlinkConfig.IDENTIFIER: FlinkSchema,
        DaskConfig.IDENTIFIER: DaskSchema,
        ContainerConfig.IDENTIFIER: ContainerSchema,
    }


class RunMixin(object):
    def get_run_kind(self):
        raise NotImplementedError()

    @property
    def has_mpi_job_run(self):
        return self.get_run_kind() == MpiJobConfig.IDENTIFIER

    @property
    def has_pytorch_job_run(self):
        return self.get_run_kind() == PytorchJobConfig.IDENTIFIER

    @property
    def has_tf_job_run(self):
        return self.get_run_kind() == TFJobConfig.IDENTIFIER

    @property
    def has_spark_run(self):
        return self.get_run_kind() == SparkConfig.IDENTIFIER

    @property
    def has_flink_run(self):
        return self.get_run_kind() == FlinkConfig.IDENTIFIER

    @property
    def has_dask_run(self):
        return self.get_run_kind() == DaskConfig.IDENTIFIER

    @property
    def has_dag_run(self):
        return self.get_run_kind() == DagConfig.IDENTIFIER

    @property
    def has_distributed_run(self):
        return self.has_mpi_job_run or self.has_pytorch_job_run or self.has_tf_job_run
