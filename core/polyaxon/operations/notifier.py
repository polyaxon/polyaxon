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
from typing import Dict, Union

from polyaxon import types
from polyaxon.auxiliaries import get_default_notification_container
from polyaxon.polyflow import (
    V1IO,
    V1Component,
    V1Notifier,
    V1Operation,
    V1Param,
    V1Plugins,
    V1Termination,
)


def get_notifier_operation(
    connection: str,
    kind: str,
    owner: str,
    project: str,
    run_uuid: str,
    run_name: str,
    condition: Union[str, Dict],
) -> V1Operation:
    return V1Operation(
        params={
            "kind": V1Param(value=kind),
            "owner": V1Param(value=owner),
            "project": V1Param(value=project),
            "run_uuid": V1Param(value=run_uuid),
            "run_name": V1Param(value=run_name),
            "condition": V1Param(value=condition),
        },
        termination=V1Termination(max_retries=3),
        component=V1Component(
            name="notifier",
            plugins=V1Plugins(
                auth=False,
                collect_logs=False,
                collect_artifacts=False,
                collect_resources=False,
                auto_resume=False,
                sync_statuses=False,
                external_host=True,
            ),
            inputs=[
                V1IO(name="kind", type=types.STR, is_optional=False),
                V1IO(name="owner", type=types.STR, is_optional=False),
                V1IO(name="project", type=types.STR, is_optional=False),
                V1IO(name="run_uuid", type=types.STR, is_optional=False),
                V1IO(name="run_name", type=types.STR, is_optional=True),
                V1IO(name="condition", type=types.DICT, is_optional=True),
                V1IO(name="connection", type=types.STR, is_optional=True),
            ],
            run=V1Notifier(
                connections=[connection],
                container=get_default_notification_container(),
            ),
        ),
    )
