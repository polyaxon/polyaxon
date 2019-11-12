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
from polyaxon.schemas.polyflow.workflows.automl.bo import BOConfig, BOSchema
from polyaxon.schemas.polyflow.workflows.automl.hyperopt import (
    HyperoptSchema,
    HyperoptConfig,
)
from polyaxon.schemas.polyflow.workflows.dag import DagConfig, DagSchema
from polyaxon.schemas.polyflow.workflows.dask import DaskConfig, DaskSchema
from polyaxon.schemas.polyflow.workflows.automl.grid_search import (
    GridSearchConfig,
    GridSearchSchema,
)
from polyaxon.schemas.polyflow.workflows.automl.hyperband import (
    HyperbandConfig,
    HyperbandSchema,
)
from polyaxon.schemas.polyflow.workflows.flink import FlinkConfig, FlinkSchema
from polyaxon.schemas.polyflow.workflows.metrics import SearchMetricSchema
from polyaxon.schemas.polyflow.workflows.automl.random_search import (
    RandomSearchConfig,
    RandomSearchSchema,
)
from polyaxon.schemas.polyflow.workflows.mapping import MappingConfig, MappingSchema
from polyaxon.schemas.polyflow.workflows.kubeflow.mpi_job import (
    MpiJobConfig,
    MpiJobSchema,
)
from polyaxon.schemas.polyflow.workflows.kubeflow.pytorch_job import (
    PytorchJobConfig,
    PytorchJobSchema,
)
from polyaxon.schemas.polyflow.workflows.kubeflow.tf_job import TFJobConfig, TFJobSchema
from polyaxon.schemas.polyflow.workflows.iterative import (
    IterativeConfig,
    IterativeSchema,
)
from polyaxon.schemas.polyflow.workflows.spark import SparkConfig, SparkSchema


class WorkflowSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MappingConfig.IDENTIFIER: MappingSchema,
        GridSearchConfig.IDENTIFIER: GridSearchSchema,
        RandomSearchConfig.IDENTIFIER: RandomSearchSchema,
        HyperbandConfig.IDENTIFIER: HyperbandSchema,
        BOConfig.IDENTIFIER: BOSchema,
        HyperoptConfig.IDENTIFIER: HyperoptSchema,
        DagConfig.IDENTIFIER: DagSchema,
        MpiJobConfig.IDENTIFIER: MpiJobSchema,
        PytorchJobConfig.IDENTIFIER: PytorchJobSchema,
        TFJobConfig.IDENTIFIER: TFJobSchema,
        SparkConfig.IDENTIFIER: SparkSchema,
        FlinkConfig.IDENTIFIER: FlinkSchema,
        DaskConfig.IDENTIFIER: DaskSchema,
        IterativeConfig.IDENTIFIER: IterativeSchema,
    }


class WorkflowMixin(object):
    def get_workflow_kind(self):
        raise NotImplementedError()

    @property
    def has_mapping_workflow(self):
        return self.get_workflow_kind() == MappingConfig.IDENTIFIER

    @property
    def has_grid_search_workflow(self):
        return self.get_workflow_kind() == GridSearchConfig.IDENTIFIER

    @property
    def has_random_search_workflow(self):
        return self.get_workflow_kind() == RandomSearchConfig.IDENTIFIER

    @property
    def has_hyperband_workflow(self):
        return self.get_workflow_kind() == HyperbandConfig.IDENTIFIER

    @property
    def has_bo_workflow(self):
        return self.get_workflow_kind() == BOConfig.IDENTIFIER

    @property
    def has_mpi_job_workflow(self):
        return self.get_workflow_kind() == MpiJobConfig.IDENTIFIER

    @property
    def has_pytorch_job_workflow(self):
        return self.get_workflow_kind() == PytorchJobConfig.IDENTIFIER

    @property
    def has_tf_job_workflow(self):
        return self.get_workflow_kind() == TFJobConfig.IDENTIFIER

    @property
    def has_spark_workflow(self):
        return self.get_workflow_kind() == SparkConfig.IDENTIFIER

    @property
    def has_flink_workflow(self):
        return self.get_workflow_kind() == FlinkConfig.IDENTIFIER

    @property
    def has_dask_workflow(self):
        return self.get_workflow_kind() == DaskConfig.IDENTIFIER

    @property
    def has_dag_workflow(self):
        return self.get_workflow_kind() == DagConfig.IDENTIFIER

    @property
    def has_distributed_workflow(self):
        return (
            self.has_mpi_job_workflow
            or self.has_pytorch_job_workflow
            or self.has_tf_job_workflow
        )

    @property
    def has_automl_workflow(self):
        return (
            self.has_mapping_workflow
            or self.has_grid_search_workflow
            or self.has_random_search_workflow
            or self.has_hyperband_workflow
            or self.has_bo_workflow
        )
