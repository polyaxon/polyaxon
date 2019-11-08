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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon.schemas.polyflow.workflows.automl.bo import BOConfig, BOSchema
from polyaxon.schemas.polyflow.workflows.dag import DagConfig, DagSchema
from polyaxon.schemas.polyflow.workflows.dask import DaskConfig, DaskSchema
from polyaxon.schemas.polyflow.workflows.early_stopping_policies import (
    EarlyStoppingSchema,
)
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
from polyaxon.schemas.polyflow.workflows.spark import SparkConfig, SparkSchema


class WorkflowStrategySchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MappingConfig.IDENTIFIER: MappingSchema,
        GridSearchConfig.IDENTIFIER: GridSearchSchema,
        RandomSearchConfig.IDENTIFIER: RandomSearchSchema,
        HyperbandConfig.IDENTIFIER: HyperbandSchema,
        BOConfig.IDENTIFIER: BOSchema,
        DagConfig.IDENTIFIER: DagSchema,
        MpiJobConfig.IDENTIFIER: MpiJobSchema,
        PytorchJobConfig.IDENTIFIER: PytorchJobSchema,
        TFJobConfig.IDENTIFIER: TFJobSchema,
        SparkConfig.IDENTIFIER: SparkSchema,
        FlinkConfig.IDENTIFIER: FlinkSchema,
        DaskConfig.IDENTIFIER: DaskSchema,
    }


class WorkflowStrategyMixin(object):
    def get_kind(self):
        raise NotImplementedError()

    @property
    def has_mapping_strategy(self):
        return self.get_kind() == MappingConfig.IDENTIFIER

    @property
    def has_grid_search_strategy(self):
        return self.get_kind() == GridSearchConfig.IDENTIFIER

    @property
    def has_random_search_strategy(self):
        return self.get_kind() == RandomSearchConfig.IDENTIFIER

    @property
    def has_hyperband_strategy(self):
        return self.get_kind() == HyperbandConfig.IDENTIFIER

    @property
    def has_bo_strategy(self):
        return self.get_kind() == BOConfig.IDENTIFIER

    @property
    def has_mpi_job_strategy(self):
        return self.get_kind() == MpiJobConfig.IDENTIFIER

    @property
    def has_pytorch_job_strategy(self):
        return self.get_kind() == PytorchJobConfig.IDENTIFIER

    @property
    def has_tf_job_strategy(self):
        return self.get_kind() == TFJobConfig.IDENTIFIER

    @property
    def has_spark_strategy(self):
        return self.get_kind() == SparkConfig.IDENTIFIER

    @property
    def has_flink_strategy(self):
        return self.get_kind() == FlinkConfig.IDENTIFIER

    @property
    def has_dask_strategy(self):
        return self.get_kind() == DaskConfig.IDENTIFIER

    @property
    def has_dag_strategy(self):
        return self.get_kind() == DagConfig.IDENTIFIER

    @property
    def has_distributed_strategy(self):
        return (
            self.has_mpi_job_strategy
            or self.has_pytorch_job_strategy
            or self.has_tf_job_strategy
        )

    @property
    def has_automl_strategy(self):
        return (
            self.has_mapping_strategy
            or self.has_grid_search_strategy
            or self.has_random_search_strategy
            or self.has_hyperband_strategy
            or self.has_bo_strategy
        )


class WorkflowSchema(BaseSchema):
    strategy = fields.Nested(WorkflowStrategySchema, required=True)
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return WorkflowConfig


class WorkflowConfig(BaseConfig, WorkflowStrategyMixin):
    SCHEMA = WorkflowSchema
    IDENTIFIER = "workflow"
    REDUCED_ATTRIBUTES = ["concurrency", "strategy", "early_stopping"]

    def __init__(self, strategy=None, concurrency=None, early_stopping=None):
        self.strategy = strategy
        self.concurrency = concurrency
        self.early_stopping = early_stopping

    def get_kind(self):
        return self.strategy.kind
