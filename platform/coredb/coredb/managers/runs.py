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

from typing import Dict, List, Set

from coredb import operations
from coredb.abstracts.getter import get_run_model
from coredb.abstracts.runs import BaseRun
from coredb.managers.statuses import new_run_status
from polyaxon.constants.metadata import META_COPY_ARTIFACTS, META_UPLOAD_ARTIFACTS
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyflow import V1CloningKind, V1CompiledOperation, V1Operation, V1RunKind
from polyaxon.schemas import V1RunPending
from polyaxon.schemas.types import V1ArtifactsType


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


def resume_run(
    run: BaseRun,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[str] = None,
    supported_kinds: Set[str] = None,
    message=None,
    **kwargs,
) -> BaseRun:
    op_spec = V1Operation.read(run.raw_content)
    instance = operations.init_run(
        project_id=run.project_id,
        user_id=user_id or run.user_id,
        name=name or run.name,
        description=description or run.description,
        readme=readme or run.readme,
        op_spec=op_spec,
        tags=tags or run.tags,
        override=content,
        supported_kinds=supported_kinds,
        **kwargs,
    ).instance

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
            type=V1Statuses.RESUMING,
            status=True,
            reason="ResumeManager",
            message=message,
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
    supported_kinds: Set[str] = None,
    **kwargs,
) -> BaseRun:
    op_spec = V1Operation.read(run.raw_content)
    meta_info = kwargs.pop("meta_info", {}) or {}
    original_meta_info = run.meta_info or {}
    original_uuid = run.uuid.hex
    upload_artifacts = original_meta_info.get(META_UPLOAD_ARTIFACTS)
    if upload_artifacts:
        meta_info[META_UPLOAD_ARTIFACTS] = upload_artifacts
    if cloning_kind == V1CloningKind.COPY and META_COPY_ARTIFACTS not in meta_info:
        # Handle default copy mode
        meta_info[META_COPY_ARTIFACTS] = V1ArtifactsType(dirs=[original_uuid]).to_dict()
    if META_COPY_ARTIFACTS not in meta_info and upload_artifacts:
        # Handle default copy mode
        meta_info[META_COPY_ARTIFACTS] = V1ArtifactsType(
            dirs=["{}/{}".format(original_uuid, upload_artifacts)]
        ).to_dict()

    instance = operations.init_run(
        project_id=run.project_id,
        user_id=user_id or run.user_id,
        name=name or run.name,
        description=description or run.description,
        readme=readme or run.readme,
        op_spec=op_spec,
        original_id=run.id,
        cloning_kind=cloning_kind,
        tags=tags or run.tags,
        override=content,
        supported_kinds=supported_kinds,
        meta_info=meta_info,
        **kwargs,
    ).instance
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
    supported_kinds: Set[str] = None,
    **kwargs,
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
        supported_kinds=supported_kinds,
        **kwargs,
    )


def copy_run(
    run: BaseRun,
    user_id: int = None,
    name: str = None,
    description: str = None,
    content: str = None,
    readme: str = None,
    tags: List[int] = None,
    supported_kinds: Set[str] = None,
    **kwargs,
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
        supported_kinds=supported_kinds,
        **kwargs,
    )


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
