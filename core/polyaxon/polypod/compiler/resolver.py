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

from typing import Dict, Optional

from polyaxon.exceptions import PolyaxonCompilerError
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler.resolvers import CoreResolver


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
):
    resolver_cls = resolver_cls or CoreResolver
    run_kind = compiled_operation.get_run_kind()
    if run_kind not in resolver_cls.KINDS:
        raise PolyaxonCompilerError(
            "Specification with run kind: {} is not supported in this deployment version.".format(
                run_kind
            )
        )

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
    )
    if resolver:
        return resolver, resolver.resolve()
