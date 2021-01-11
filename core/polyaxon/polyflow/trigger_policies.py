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

from polyaxon.lifecycle import V1Statuses


class V1TriggerPolicy(polyaxon_sdk.V1TriggerPolicy):
    trigger_statuses_mapping = {
        polyaxon_sdk.V1TriggerPolicy.ALL_SUCCEEDED: V1Statuses.SUCCEEDED,
        polyaxon_sdk.V1TriggerPolicy.ALL_FAILED: V1Statuses.FAILED,
        polyaxon_sdk.V1TriggerPolicy.ALL_DONE: V1Statuses.DONE,
        polyaxon_sdk.V1TriggerPolicy.ONE_SUCCEEDED: V1Statuses.SUCCEEDED,
        polyaxon_sdk.V1TriggerPolicy.ONE_FAILED: V1Statuses.FAILED,
        polyaxon_sdk.V1TriggerPolicy.ONE_DONE: V1Statuses.DONE,
    }
