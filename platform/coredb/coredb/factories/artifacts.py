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

import factory

from coredb.abstracts.getter import get_artifact_model
from polyaxon_sdk import V1ArtifactKind


class ArtifactFactory(factory.django.DjangoModelFactory):
    name = "accuracy"
    kind = V1ArtifactKind.METRIC
    summary = {"last_value": 0.9, "max_value": 0.9, "min_value": 0.1}
    path = "accuracy"

    class Meta:
        model = get_artifact_model()
