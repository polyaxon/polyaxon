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
from datetime import datetime
from typing import Dict, List, Optional

from polyaxon.polyflow import V1IO, V1CloningKind, V1CompiledOperation, V1Operation
from polyaxon.polypod.compiler.resolver.base import BaseResolver


def resolve(
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_name: str,
    run_uuid: str,
    run_path: str,
    compiled_operation: V1CompiledOperation,
    params: Optional[Dict[str, Dict]],
    run=None,
    resolver_cls=None,
    created_at: datetime = None,
    compiled_at: datetime = None,
    cloning_kind: V1CloningKind = None,
    original_uuid: str = None,
    is_independent: bool = True,
    eager: bool = False,
):
    resolver_cls = resolver_cls or BaseResolver
    resolver_cls.is_valid(compiled_operation)

    resolver = resolver_cls(
        run=run,
        compiled_operation=compiled_operation,
        owner_name=owner_name,
        project_name=project_name,
        project_uuid=project_uuid,
        run_name=run_name,
        run_path=run_path,
        run_uuid=run_uuid,
        params=params,
        created_at=created_at,
        compiled_at=compiled_at,
        cloning_kind=cloning_kind,
        original_uuid=original_uuid,
        is_independent=is_independent,
        eager=eager,
    )
    if resolver:
        # If build section is present resolve the build
        if compiled_operation.build:
            return resolver, resolver.resolve_build()
        return resolver, resolver.resolve()


def resolve_hooks(
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_name: str,
    run_uuid: str,
    run_path: str,
    compiled_operation: V1CompiledOperation,
    params: Optional[Dict[str, Dict]],
    run=None,
    resolver_cls=None,
    created_at: datetime = None,
    compiled_at: datetime = None,
    cloning_kind: V1CloningKind = None,
    original_uuid: str = None,
    eager: bool = False,
) -> List[V1Operation]:
    resolver_cls = resolver_cls or BaseResolver
    resolver_cls.is_valid(compiled_operation)

    if run:
        # Add outputs to compiled operation
        compiled_operation.outputs = [
            V1IO(name=k, type=None, value=v, is_optional=True)
            for k, v in (run.outputs or {}).items()
        ]
    return resolver_cls(
        run=run,
        compiled_operation=compiled_operation,
        owner_name=owner_name,
        project_name=project_name,
        project_uuid=project_uuid,
        run_uuid=run_uuid,
        run_name=run_name,
        run_path=run_path,
        params=params,
        compiled_at=compiled_at,
        created_at=created_at,
        cloning_kind=cloning_kind,
        original_uuid=original_uuid,
        is_independent=False,
        eager=eager,
    ).resolve_hooks()
