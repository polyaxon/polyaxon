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

from typing import Dict, Set, Union

from coredb import operations
from coredb.abstracts.runs import BaseRun
from polyaxon.polyflow import V1CompiledOperation, V1Operation


def compile_operation_run(
    project_id: int,
    user_id: int,
    op_spec: V1Operation = None,
    compiled_operation: V1CompiledOperation = None,
    name: str = None,
    description: str = None,
    tags: str = None,
    override: Union[str, Dict] = None,
    override_post: bool = True,
    params: Dict = None,
    readme: str = None,
    is_managed: bool = True,
    pipeline_id: int = None,
    controller_id: int = None,
    supported_kinds: Set[str] = None,
) -> BaseRun:
    compiled_operation, instance = operations.init_run(
        project_id=project_id,
        user_id=user_id,
        name=name,
        description=description,
        op_spec=op_spec,
        compiled_operation=compiled_operation,
        override=override,
        override_post=override_post,
        params=params,
        readme=readme,
        pipeline_id=pipeline_id,
        controller_id=controller_id,
        tags=tags,
        is_managed=is_managed,
        supported_kinds=supported_kinds,
    )
    instance.save()
    return instance
