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

STATS_RUN = [
    "id",
    "uuid",
    "name",
    "kind",
    "created_at",
    "updated_at",
    "started_at",
    "finished_at",
    "status",
    "inputs",
    "outputs",
    "tags",
]
STATUS_UPDATE_COLUMNS_ONLY = [
    "id",
    "status",
    "status_conditions",
    "started_at",
    "updated_at",
    "finished_at",
    "duration",
    "meta_info",
]
STATUS_UPDATE_COLUMNS_DEFER = [
    "original",
    "cloning_kind",
    "description",
    "inputs",
    "outputs",
    "tags",
    "description",
    "live_state",
    "readme",
    "content",
    "is_managed",
    "is_approved",
]
DEFAULT_COLUMNS_DEFER = ["description", "readme", "content", "raw_content"]
