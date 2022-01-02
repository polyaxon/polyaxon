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

from typing import Dict, List

from coredb.abstracts.getter import get_run_model
from coredb.abstracts.runs import BaseRun
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyflow import V1CompiledOperation, V1RunKind
from polyaxon.schemas import V1RunPending


def create_run(
    project_id: int,
    user_id: int,
    name: str = None,
    description: str = None,
    readme: str = None,
    tags: List[int] = None,
    raw_content: str = None,
    meta_info: Dict = None,
) -> BaseRun:
    instance = get_run_model().objects.create(
        project_id=project_id,
        user_id=user_id,
        name=name,
        description=description,
        readme=readme,
        tags=tags,
        kind=V1RunKind.JOB,
        is_managed=False,
        raw_content=raw_content,
        meta_info=meta_info,
        status_conditions=[
            V1StatusCondition.get_condition(
                type=V1Statuses.CREATED,
                status="True",
                reason="ModelManager",
                message="Run is created",
            ).to_dict()
        ],
    )
    return instance


def base_approve_run(run: BaseRun):
    pending = run.pending
    if pending:
        new_pending = None
        if (
            (pending == V1RunPending.BUILD and run.status == V1Statuses.CREATED)
            or pending == V1RunPending.UPLOAD
        ) and run.content:
            compiled_operation = V1CompiledOperation.read(run.content)
            if compiled_operation.is_approved is False:
                new_pending = V1RunPending.APPROVAL
        run.pending = new_pending
        run.save(update_fields=["pending", "updated_at"])
