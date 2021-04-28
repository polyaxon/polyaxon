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
from typing import List

from polyaxon.auxiliaries import get_default_cleaner_container
from polyaxon.auxiliaries.cleaner import get_batch_cleaner_container
from polyaxon.polyflow import (
    V1CleanerJob,
    V1Component,
    V1Operation,
    V1Plugins,
    V1Termination,
)
from polyaxon.schemas.types import V1ConnectionType


def get_cleaner_operation(
    connection: V1ConnectionType, run_uuid: str, run_kind: str
) -> V1Operation:
    return V1Operation(
        termination=V1Termination(max_retries=1),
        component=V1Component(
            name="cleaner",
            plugins=V1Plugins(
                auth=False,
                collect_logs=False,
                collect_artifacts=False,
                collect_resources=False,
                auto_resume=False,
                sync_statuses=False,
            ),
            run=V1CleanerJob(
                connections=[connection.name],
                container=get_default_cleaner_container(connection, run_uuid, run_kind),
            ),
        ),
    )


def get_batch_cleaner_operation(
    connection: V1ConnectionType,
    paths: List[str],
) -> V1Operation:
    return V1Operation(
        termination=V1Termination(max_retries=1),
        component=V1Component(
            name="cleaner",
            plugins=V1Plugins(
                auth=False,
                collect_logs=False,
                collect_artifacts=False,
                collect_resources=False,
                auto_resume=False,
                sync_statuses=False,
            ),
            run=V1CleanerJob(
                connections=[connection.name],
                container=get_batch_cleaner_container(connection, paths),
            ),
        ),
    )
