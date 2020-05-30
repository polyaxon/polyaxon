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

from polycommon.apis.regex import (
    ARTIFACT_NAME_PATTERN,
    OWNER_NAME_PATTERN,
    PROJECT_NAME_PATTERN,
    RUN_UUID_PATTERN,
)

URLS_RUNS_CREATE = r"^{}/{}/runs/create/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_RUNS_LIST = r"^{}/runs/list/?$".format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN)
URLS_RUNS_DETAILS = r"^{}/{}/runs/{}/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_RESTART = r"^{}/{}/runs/{}/restart/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_RESUME = r"^{}/{}/runs/{}/resume/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_COPY = r"^{}/{}/runs/{}/copy/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_STOP = r"^{}/{}/runs/{}/stop/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_STATUSES = r"^{}/{}/runs/{}/statuses/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_NAMESPACE = r"^{}/{}/runs/{}/namespace/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_ARTIFACTS_LINEAGE_LIST = r"^{}/{}/runs/{}/artifacts_lineage/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_ARTIFACTS_LINEAGE_NAMES = r"^{}/{}/runs/{}/artifacts_lineage/names/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN
)
URLS_RUNS_ARTIFACTS_LINEAGE_DETAILS = r"^{}/{}/runs/{}/artifacts_lineage/{}/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN, RUN_UUID_PATTERN, ARTIFACT_NAME_PATTERN
)
