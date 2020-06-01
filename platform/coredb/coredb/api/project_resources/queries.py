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

from coredb.models.runs import Run

runs = Run.all.select_related("original")
runs = runs.only(
    "original__id",
    "original__uuid",
    "original__name",
    "user__username",
    "id",
    "uuid",
    "name",
    "kind",
    "meta_info",
    "description",
    "created_at",
    "updated_at",
    "started_at",
    "finished_at",
    "status",
    "cloning_kind",
    "is_managed",
    "inputs",
    "outputs",
    "tags",
    "deleted",
)
