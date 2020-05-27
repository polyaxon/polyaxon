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

import polyaxon_sdk


class V1MatrixKind(polyaxon_sdk.V1MatrixKind):
    CHOICES = (
        (polyaxon_sdk.V1MatrixKind.RANDOM, polyaxon_sdk.V1MatrixKind.RANDOM),
        (polyaxon_sdk.V1MatrixKind.GRID, polyaxon_sdk.V1MatrixKind.GRID),
        (polyaxon_sdk.V1MatrixKind.HYPERBAND, polyaxon_sdk.V1MatrixKind.HYPERBAND),
        (polyaxon_sdk.V1MatrixKind.BAYES, polyaxon_sdk.V1MatrixKind.BAYES),
        (polyaxon_sdk.V1MatrixKind.HYPEROPT, polyaxon_sdk.V1MatrixKind.HYPEROPT),
        (polyaxon_sdk.V1MatrixKind.ITERATIVE, polyaxon_sdk.V1MatrixKind.ITERATIVE),
        (polyaxon_sdk.V1MatrixKind.MAPPING, polyaxon_sdk.V1MatrixKind.MAPPING),
    )
