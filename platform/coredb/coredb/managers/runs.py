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

from typing import List

from coredb import operations
from coredb.abstracts.getter import get_run_model
from coredb.abstracts.runs import BaseRun
from coredb.managers.statuses import new_run_status
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyflow import V1CloningKind, V1Operation, V1RunKind


def create_run(
    project_id: int,
    user_id: int,
    name: str = None,
    description: str = None,
    readme: str = None,
    tags: List[int] = None,
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
        status_conditions=[
            V1StatusCondition.get_condition(
                type=V1Statuses.CREATED,
                status="True",
                reason="PolyaxonRunCreated",
                message="Run is created",
            ).to_dict()
        ],
    )
    return instance


def resume_run(
    run: BaseRun,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[str] = None,
) -> BaseRun:
    op_spec = V1Operation.read(run.raw_content)
    compiled_operation, instance = operations.init_run(
        project_id=run.project_id,
        user_id=user_id or run.user_id,
        name=name or run.name,
        description=description or run.description,
        readme=readme or run.readme,
        op_spec=op_spec,
        tags=tags or run.tags,
        override=content,
        override_post=True,
    )

    run.user_id = instance.user_id
    run.name = instance.name
    run.description = instance.description
    run.readme = instance.readme
    run.content = instance.content
    run.raw_content = instance.raw_content
    run.tags = instance.tags
    run.save()
    new_run_status(
        run,
        condition=V1StatusCondition.get_condition(
            type=V1Statuses.RESUMING, status=True
        ),
    )
    return run


def clone_run(
    run: BaseRun,
    cloning_kind: str,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[int] = None,
) -> BaseRun:
    op_spec = V1Operation.read(run.raw_content)
    compiled_operation, instance = operations.init_run(
        project_id=run.project_id,
        user_id=user_id or run.user_id,
        name=name or run.name,
        description=description or run.description,
        readme=readme or run.readme,
        op_spec=op_spec,
        original_id=run.id,
        original_uuid=run.uuid.hex,
        cloning_kind=cloning_kind,
        tags=tags or run.tags,
        override=content,
        override_post=True,
    )
    instance.save()
    return instance


def restart_run(
    run: BaseRun,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[int] = None,
) -> BaseRun:
    return clone_run(
        run=run,
        cloning_kind=V1CloningKind.RESTART,
        user_id=user_id,
        name=name,
        description=description,
        content=content,
        readme=readme,
        tags=tags,
    )


def copy_run(
    run: BaseRun,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[int] = None,
) -> BaseRun:
    return clone_run(
        run=run,
        cloning_kind=V1CloningKind.COPY,
        user_id=user_id,
        name=name,
        description=description,
        content=content,
        readme=readme,
        tags=tags,
    )
