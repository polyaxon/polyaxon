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

from polyaxon.polyboard.artifacts import V1RunArtifact
from polyaxon.polyflow import ParamSpec, V1CompiledOperation
from polyaxon.polypod.compiler.lineage.io_collector import collect_io_artifacts
from polyaxon.schemas.types import V1ConnectionType


def resolve_artifacts_lineage(
    owner_name: str,
    project_name: str,
    project_uuid: str,
    run_uuid: str,
    run_name: str,
    run_path: str,
    param_spec: Dict[str, ParamSpec],
    compiled_operation: V1CompiledOperation,
    artifacts_store: V1ConnectionType,
    connection_by_names: Dict[str, V1ConnectionType],
) -> List[V1RunArtifact]:
    return collect_io_artifacts(
        compiled_operation=compiled_operation, connection_by_names=connection_by_names
    )
