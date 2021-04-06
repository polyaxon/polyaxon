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

from polyaxon.polyflow.cache import CacheSchema, V1Cache
from polyaxon.polyflow.component import ComponentSchema, V1Component
from polyaxon.polyflow.dags import DagOpSpec
from polyaxon.polyflow.early_stopping import (
    DiffStoppingPolicySchema,
    EarlyStoppingSchema,
    FailureEarlyStoppingSchema,
    MedianStoppingPolicySchema,
    MetricEarlyStoppingSchema,
    StoppingPolicySchema,
    TruncationStoppingPolicySchema,
    V1DiffStoppingPolicy,
    V1FailureEarlyStopping,
    V1MedianStoppingPolicy,
    V1MetricEarlyStopping,
    V1TruncationStoppingPolicy,
)
from polyaxon.polyflow.environment import EnvironmentSchema, V1Environment
from polyaxon.polyflow.events import EventTriggerSchema, V1EventKind, V1EventTrigger
from polyaxon.polyflow.hooks import HookSchema, V1Hook
from polyaxon.polyflow.init import InitSchema, V1Init
from polyaxon.polyflow.io import V1IO, IOSchema
from polyaxon.polyflow.joins import JoinParamSchema, JoinSchema, V1Join, V1JoinParam
from polyaxon.polyflow.matrix import (
    AcquisitionFunctions,
    BayesSchema,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    GridSearchSchema,
    HyperbandSchema,
    HyperoptSchema,
    IterativeSchema,
    MappingSchema,
    MatrixMixin,
    MatrixSchema,
    RandomSearchSchema,
    UtilityFunctionConfig,
    V1Bayes,
    V1GridSearch,
    V1HpChoice,
    V1HpGeomSpace,
    V1HpLinSpace,
    V1HpLogNormal,
    V1HpLogSpace,
    V1HpLogUniform,
    V1HpNormal,
    V1HpPChoice,
    V1HpQLogNormal,
    V1HpQLogUniform,
    V1HpQNormal,
    V1HpQUniform,
    V1HpRange,
    V1HpUniform,
    V1Hyperband,
    V1Hyperopt,
    V1Iterative,
    V1Mapping,
    V1Matrix,
    V1MatrixKind,
    V1RandomSearch,
    V1Tuner,
)
from polyaxon.polyflow.mounts import ArtifactsMountSchema, V1ArtifactsMount
from polyaxon.polyflow.notifications import NotificationSchema, V1Notification
from polyaxon.polyflow.operations import (
    CompiledOperationSchema,
    OperationSchema,
    V1CompiledOperation,
    V1Operation,
)
from polyaxon.polyflow.operators import ForConfig, IfConfig
from polyaxon.polyflow.optimization import (
    OptimizationMetricSchema,
    OptimizationResourceSchema,
    ResourceType,
    V1Optimization,
    V1OptimizationMetric,
    V1OptimizationResource,
)
from polyaxon.polyflow.params import ParamSpec, V1Param, ops_params
from polyaxon.polyflow.plugins import PluginsSchema, V1Plugins
from polyaxon.polyflow.references import (
    DagRefSchema,
    HubRefSchema,
    PathRefSchema,
    RefMixin,
    UrlRefSchema,
    V1DagRef,
    V1HubRef,
    V1PathRef,
    V1UrlRef,
)
from polyaxon.polyflow.run import (
    CleanerJobSchema,
    DagSchema,
    DaskSchema,
    FlinkSchema,
    JobSchema,
    KFReplicaSchema,
    MPIJobSchema,
    NotifierJobSchema,
    PytorchJobSchema,
    RunMixin,
    RunSchema,
    ServiceSchema,
    SparkReplicaSchema,
    SparkSchema,
    TFJobSchema,
    TunerJobSchema,
    V1CleanerJob,
    V1CleanPodPolicy,
    V1CloningKind,
    V1Dag,
    V1Dask,
    V1Flink,
    V1Job,
    V1KFReplica,
    V1MPIJob,
    V1NotifierJob,
    V1PipelineKind,
    V1PytorchJob,
    V1RunEdgeKind,
    V1RunKind,
    V1Service,
    V1Spark,
    V1SparkDeploy,
    V1SparkReplica,
    V1SparkType,
    V1TFJob,
    V1TunerJob,
    validate_run_patch,
)
from polyaxon.polyflow.schedules import (
    CronScheduleSchema,
    DateTimeScheduleSchema,
    IntervalScheduleSchema,
    ScheduleMixin,
    ScheduleSchema,
    V1CronSchedule,
    V1DateTimeSchedule,
    V1IntervalSchedule,
    V1ScheduleKind,
)
from polyaxon.polyflow.templates import TemplateSchema, V1Template
from polyaxon.polyflow.termination import TerminationSchema, V1Termination
from polyaxon.polyflow.trigger_policies import V1TriggerPolicy
