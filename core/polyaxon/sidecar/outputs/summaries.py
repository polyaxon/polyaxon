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
import os

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from polyaxon.client import RunClient
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_RUN_EVENTS_FORMAT,
)
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyboard.events import V1Events
from polyaxon.stores.manager import get_artifacts_connection
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.path_utils import (
    get_dirs_under_path,
    get_files_in_path_context,
    get_path,
)


def sync_summaries(last_check: Optional[datetime], run_uuid: str, client: RunClient):
    events_path = CONTEXT_MOUNT_RUN_EVENTS_FORMAT.format(run_uuid)
    # check if there's a path to sync
    if not os.path.exists(events_path):
        return

    # crawl dirs
    summaries = []
    last_values = {}
    connection = get_artifacts_connection()
    connection_name = connection.name if connection else None

    for events_kind in get_dirs_under_path(events_path):
        _summaries, _last_values = sync_events_summaries(
            events_path=events_path,
            events_kind=events_kind,
            last_check=last_check,
            connection_name=connection_name,
        )
        summaries += _summaries
        last_values.update(_last_values)

    if summaries:
        client.log_artifact_lineage(summaries)
    if last_values:
        client.log_outputs(**last_values)


def sync_events_summaries(
    events_path: str,
    events_kind: str,
    last_check: Optional[datetime],
    connection_name: str = None,
) -> Tuple[List, Dict]:
    current_events_path = get_path(events_path, events_kind)

    summaries = []
    last_values = {}
    with get_files_in_path_context(current_events_path) as files:
        for f in files:
            if last_check and not file_modified_since(filepath=f, last_time=last_check):
                continue

            event_name = os.path.basename(f).split(".plx")[0]
            event = V1Events.read(kind=events_kind, name=event_name, data=f)
            if event.df.empty:
                continue

            # Get only the relpath from run uuid
            event_rel_path = os.path.relpath(f, CONTEXT_MOUNT_ARTIFACTS)
            summary = event.get_summary()
            run_artifact = V1RunArtifact(
                name=event_name,
                kind=events_kind,
                connection=connection_name,
                summary=summary,
                path=event_rel_path,
                is_input=False,
            )
            summaries.append(run_artifact)
            if events_kind == V1ArtifactKind.METRIC:
                last_values[event_name] = summary[V1ArtifactKind.METRIC]["last"]

    return summaries, last_values
