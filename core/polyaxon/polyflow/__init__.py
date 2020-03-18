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

from polyaxon.polyflow.dags import DagOpSpec
from polyaxon.polyflow.io.params import (
    V1ParamSearch,
    V1Param,
    ParamSpec,
    DAG_ENTITY_REF,
    validate_params,
)
from polyaxon.polyflow.component import (
    ComponentSchema,
    V1Component,
)
from polyaxon.polyflow.cache import (
    V1Cache,
    CacheSchema,
)
from polyaxon.polyflow.conditions import (
    V1IoCond,
    IoCondSchema,
    V1StatusCond,
    StatusCondSchema,
    ConditionSchema,
)
from polyaxon.polyflow.early_stopping import (
    FailureEarlyStoppingSchema,
    MetricEarlyStoppingSchema,
    V1MetricEarlyStopping,
    V1FailureEarlyStopping,
    MedianStoppingPolicySchema,
    V1MedianStoppingPolicy,
    DiffStoppingPolicySchema,
    V1DiffStoppingPolicy,
    TruncationStoppingPolicySchema,
    V1TruncationStoppingPolicy,
    StoppingPolicySchema,
    MetricEarlyStoppingSchema,
    V1MetricEarlyStopping,
    FailureEarlyStoppingSchema,
    V1FailureEarlyStopping,
    EarlyStoppingSchema,
)
from polyaxon.polyflow.environment import EnvironmentSchema, V1Environment
from polyaxon.polyflow.plugins import (
    PluginsSchema,
    V1Plugins,
)
from polyaxon.polyflow.notifications import (
    V1Notification,
    NotificationSchema,
    V1NotificationTrigger,
)
from polyaxon.polyflow.init import InitSchema, V1Init
from polyaxon.polyflow.io import IOSchema, V1IO
from polyaxon.polyflow.mounts import ArtifactsMountSchema, V1ArtifactsMount
from polyaxon.polyflow.operations import (
    OperationSchema,
    V1Operation,
    CompiledOperationSchema,
    V1CompiledOperation,
)
from polyaxon.polyflow.optimization import (
    ResourceType,
    Optimization,
    OptimizationMetricSchema,
    V1OptimizationMetric,
    OptimizationResourceSchema,
    V1OptimizationResource,
)
from polyaxon.polyflow.parallel import (
    V1Bayes,
    BayesSchema,
    V1GridSearch,
    GridSearchSchema,
    V1Hyperband,
    HyperbandSchema,
    HyperoptSchema,
    V1Hyperopt,
    V1RandomSearch,
    RandomSearchSchema,
    V1Iterative,
    IterativeSchema,
    V1Mapping,
    MappingSchema,
    ParallelSchema,
    ParallelMixin,
    UtilityFunctionConfig,
    AcquisitionFunctions,
    GaussianProcessConfig,
    GaussianProcessesKernels,
)
from polyaxon.polyflow.parallel.matrix import (
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
from polyaxon.polyflow.references import (
    DagReferenceSchema,
    V1DagReference,
    HubReferenceSchema,
    V1HubReference,
    PathReferenceSchema,
    V1PathReference,
    UrlReferenceSchema,
    V1UrlReference,
    RefMixin,
)
from polyaxon.polyflow.run import (
    V1CleanPodPolicy,
    V1Job,
    JobSchema,
    V1KFReplica,
    KFReplicaSchema,
    ServiceSchema,
    V1Service,
    V1Dag,
    DagSchema,
    V1Dask,
    DaskSchema,
    V1Flink,
    FlinkSchema,
    V1MPIJob,
    MPIJobSchema,
    V1PytorchJob,
    PytorchJobSchema,
    V1TFJob,
    TFJobSchema,
    V1SparkReplica,
    SparkReplicaSchema,
    V1Spark,
    V1SparkType,
    V1SparkDeploy,
    SparkSchema,
    RunSchema,
    RunMixin,
    V1RunKind,
    V1CloningKind,
    V1PipelineKind,
)
from polyaxon.polyflow.schedule import (
    V1CronSchedule,
    CronScheduleSchema,
    V1ExactTimeSchedule,
    ExactTimeScheduleSchema,
    V1IntervalSchedule,
    IntervalScheduleSchema,
    V1RepeatableSchedule,
    RepeatableScheduleSchema,
    ScheduleSchema,
    ScheduleMixin,
)
from polyaxon.polyflow.termination import TerminationSchema, V1Termination
from polyaxon.polyflow.operators import ForConfig, IfConfig
from polyaxon.polyflow.trigger_policies import V1TriggerPolicy
