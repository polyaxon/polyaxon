#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polycommon.apis.regex import OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN

# Projects
URLS_PROJECTS_CREATE = r"^{}/projects/create/?$".format(OWNER_NAME_PATTERN)
URLS_PROJECTS_LIST = r"^{}/projects/list/?$".format(OWNER_NAME_PATTERN)
URLS_PROJECTS_NAMES = r"^{}/projects/names/?$".format(OWNER_NAME_PATTERN)
URLS_PROJECTS_DETAILS = r"^{}/{}/?$".format(OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN)

# Resources
URLS_PROJECTS_RUNS_TAG = r"^{}/{}/runs/tag/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_STOP = r"^{}/{}/runs/stop/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_APPROVE = r"^{}/{}/runs/approve/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_DELETE = r"^{}/{}/runs/delete/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_SYNC = r"^{}/{}/runs/sync/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_ARTIFACTS_LINEAGE_V0 = r"^{}/{}/runs/artifacts_lineage/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_ARTIFACTS_LINEAGE = r"^{}/{}/runs/lineage/artifacts/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
URLS_PROJECTS_RUNS_LIST = r"^{}/{}/runs/?$".format(
    OWNER_NAME_PATTERN, PROJECT_NAME_PATTERN
)
