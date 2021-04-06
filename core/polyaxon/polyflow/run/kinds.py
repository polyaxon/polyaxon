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

import polyaxon_sdk


class V1RunKind(polyaxon_sdk.V1RunKind):
    eager_values = {
        polyaxon_sdk.V1RunKind.MATRIX,
    }
    default_runtime_values = {
        polyaxon_sdk.V1RunKind.JOB,
        polyaxon_sdk.V1RunKind.SERVICE,
        polyaxon_sdk.V1RunKind.MPIJOB,
        polyaxon_sdk.V1RunKind.TFJOB,
        polyaxon_sdk.V1RunKind.PYTORCHJOB,
        polyaxon_sdk.V1RunKind.NOTIFIER,
        polyaxon_sdk.V1RunKind.WATCHDOG,
        polyaxon_sdk.V1RunKind.TUNER,
        polyaxon_sdk.V1RunKind.CLEANER,
    }


class V1CloningKind(polyaxon_sdk.V1CloningKind):
    pass


class V1PipelineKind(polyaxon_sdk.V1PipelineKind):
    pass


class V1RunEdgeKind(polyaxon_sdk.V1RunEdgeKind):
    pass
