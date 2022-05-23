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

# To keep backwards compatibility

from typing import List, Optional

from polyaxon.client import RunClient
from traceml import tracking
from traceml.tracking import *

TRACKING_RUN = None


def init(
    owner: str = None,
    project: str = None,
    run_uuid: str = None,
    client: RunClient = None,
    track_code: bool = True,
    track_env: bool = True,
    refresh_data: bool = False,
    artifacts_path: str = None,
    collect_artifacts: str = None,
    collect_resources: str = None,
    is_offline: bool = None,
    is_new: bool = None,
    name: str = None,
    description: str = None,
    tags: List[str] = None,
) -> Optional[Run]:
    global TRACKING_RUN

    TRACKING_RUN = tracking.init(
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        client=client,
        track_code=track_code,
        track_env=track_env,
        refresh_data=refresh_data,
        artifacts_path=artifacts_path,
        collect_artifacts=collect_artifacts,
        collect_resources=collect_resources,
        is_offline=is_offline,
        is_new=is_new,
        name=name,
        description=description,
        tags=tags,
    )
    return TRACKING_RUN


def get_or_create_run(tracking_run: Run = None) -> Optional[Run]:
    global TRACKING_RUN

    TRACKING_RUN = tracking.get_or_create_run(tracking_run)
    return TRACKING_RUN
