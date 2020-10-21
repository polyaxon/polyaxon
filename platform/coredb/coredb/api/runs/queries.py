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

from coredb.api.project_resources import queries
from coredb.models.runs import Run
from coredb.queries.runs import API_COLUMNS_DEFER

single_run = queries.runs.prefetch_related(
    "project",
)
deferred_runs = Run.objects.defer(*API_COLUMNS_DEFER).prefetch_related(
    "project",
)
