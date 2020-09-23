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

SINGLE_RUN = [
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
    "live_state",
]
STATUS_UPDATE_COLUMNS_DEFER = [
    "original",
    "cloning_kind",
    "meta_info",
    "description",
    "inputs",
    "outputs",
    "tags",
    "description",
    "live_state",
    "readme",
    "content",
]
API_COLUMNS_DEFER = [
    "original",
    "cloning_kind",
    "user",
    "kind",
    "meta_info",
    "description",
    "created_at",
    "updated_at",
    "started_at",
    "finished_at",
    "duration",
    "status",
    "status_conditions",
    "inputs",
    "outputs",
    "tags",
    "description",
    "live_state",
    "readme",
    "content",
]
