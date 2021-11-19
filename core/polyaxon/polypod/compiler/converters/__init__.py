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

from polyaxon.polyflow import V1RunKind
from polyaxon.polypod.compiler.converters.base import BaseConverter, ConverterAbstract
from polyaxon.polypod.compiler.converters.helpers import (
    CleanerConverter,
    NotifierConverter,
    PlatformCleanerConverter,
    PlatformNotifierConverter,
    PlatformTunerConverter,
    TunerConverter,
)
from polyaxon.polypod.compiler.converters.job import JobConverter, PlatformJobConverter
from polyaxon.polypod.compiler.converters.kubeflow import (
    MPIJobConverter,
    MXJobConverter,
    PytorchJobConverter,
    TfJobConverter,
    XGBoostJobConverter,
)
from polyaxon.polypod.compiler.converters.kubeflow.mpi_job import (
    PlatformMPIJobConverter,
)
from polyaxon.polypod.compiler.converters.kubeflow.mx_job import PlatformMXJobConverter
from polyaxon.polypod.compiler.converters.kubeflow.pytroch_job import (
    PlatformPytorchJobConverter,
)
from polyaxon.polypod.compiler.converters.kubeflow.tf_job import PlatformTfJobConverter
from polyaxon.polypod.compiler.converters.kubeflow.xgboost_job import (
    PlatformXGBoostJobConverter,
)
from polyaxon.polypod.compiler.converters.service import (
    PlatformServiceConverter,
    ServiceConverter,
)

CORE_CONVERTERS = {
    V1RunKind.CLEANER: CleanerConverter,
    V1RunKind.NOTIFIER: NotifierConverter,
    V1RunKind.TUNER: TunerConverter,
    V1RunKind.JOB: JobConverter,
    V1RunKind.SERVICE: ServiceConverter,
    V1RunKind.MPIJOB: MPIJobConverter,
    V1RunKind.TFJOB: TfJobConverter,
    V1RunKind.XGBJOB: XGBoostJobConverter,
    V1RunKind.MXJOB: MXJobConverter,
    V1RunKind.PYTORCHJOB: PytorchJobConverter,
}

PLATFORM_CONVERTERS = {
    V1RunKind.CLEANER: PlatformCleanerConverter,
    V1RunKind.NOTIFIER: PlatformNotifierConverter,
    V1RunKind.TUNER: PlatformTunerConverter,
    V1RunKind.JOB: PlatformJobConverter,
    V1RunKind.SERVICE: PlatformServiceConverter,
    V1RunKind.MPIJOB: PlatformMPIJobConverter,
    V1RunKind.TFJOB: PlatformTfJobConverter,
    V1RunKind.PYTORCHJOB: PlatformPytorchJobConverter,
    V1RunKind.MXJOB: PlatformMXJobConverter,
    V1RunKind.XGBJOB: PlatformXGBoostJobConverter,
}
