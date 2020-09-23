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

from polyaxon.polyflow.actions import (
    ActionSchema,
    V1Action,
)
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
from polyaxon.polyflow.hooks import (
    HookSchema,
    V1Hook,
    V1HookTrigger,
)
from polyaxon.polyflow.init import InitSchema, V1Init
from polyaxon.polyflow.io import V1IO, IOSchema
from polyaxon.polyflow.mounts import ArtifactsMountSchema, V1ArtifactsMount
from polyaxon.polyflow.notifications import (
    NotificationSchema,
    V1Notification,
    V1NotificationTrigger,
)
from polyaxon.polyflow.operations import (
    CompiledOperationSchema,
    OperationSchema,
    V1CompiledOperation,
    V1Operation,
)
from polyaxon.polyflow.operators import ForConfig, IfConfig
from polyaxon.polyflow.optimization import (
    V1Optimization,
    OptimizationMetricSchema,
    OptimizationResourceSchema,
    ResourceType,
    V1OptimizationMetric,
    V1OptimizationResource,
)
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
    V1Hyperband,
    V1Hyperopt,
    V1Iterative,
    V1Mapping,
    V1RandomSearch,
    V1Matrix,
    V1MatrixKind,
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
)
from polyaxon.polyflow.params import (
    ops_params,
    DAG_ENTITY_REF,
    ParamSpec,
    V1Param,
    V1ParamSearch,
)
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
    DagSchema,
    DaskSchema,
    FlinkSchema,
    JobSchema,
    KFReplicaSchema,
    MPIJobSchema,
    NotifierSchema,
    PytorchJobSchema,
    RunMixin,
    RunSchema,
    ServiceSchema,
    SparkReplicaSchema,
    SparkSchema,
    TFJobSchema,
    TunerSchema,
    validate_run_patch,
    V1CleanPodPolicy,
    V1CloningKind,
    V1Dag,
    V1Dask,
    V1Flink,
    V1Job,
    V1KFReplica,
    V1MPIJob,
    V1Notifier,
    V1PipelineKind,
    V1PytorchJob,
    V1RunKind,
    V1Service,
    V1Spark,
    V1SparkDeploy,
    V1SparkReplica,
    V1SparkType,
    V1TFJob,
    V1Tuner,
)
from polyaxon.polyflow.schedule import (
    CronScheduleSchema,
    ExactTimeScheduleSchema,
    IntervalScheduleSchema,
    RepeatableScheduleSchema,
    ScheduleMixin,
    ScheduleSchema,
    V1CronSchedule,
    V1ExactTimeSchedule,
    V1IntervalSchedule,
    V1RepeatableSchedule,
)
from polyaxon.polyflow.termination import TerminationSchema, V1Termination
from polyaxon.polyflow.templates import TemplateSchema, V1Template
from polyaxon.polyflow.trigger_policies import V1TriggerPolicy
