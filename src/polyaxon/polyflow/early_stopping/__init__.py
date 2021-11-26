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

from polyaxon.polyflow.early_stopping.policies import (
    DiffStoppingPolicySchema,
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
from polyaxon.schemas.base import BaseOneOfSchema


class EarlyStoppingSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1MetricEarlyStopping.IDENTIFIER: MetricEarlyStoppingSchema,
        V1FailureEarlyStopping.IDENTIFIER: FailureEarlyStoppingSchema,
    }
