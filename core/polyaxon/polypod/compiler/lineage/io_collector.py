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

from typing import Dict, List, Optional

from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyflow import V1IO, V1CompiledOperation
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.types import IMAGE, LINEAGE_VALUES
from polyaxon.utils.list_utils import to_list


def collect_artifacts_from_io(
    io: V1IO, connection_by_names: Dict[str, V1ConnectionType], is_input: bool
) -> Optional[V1RunArtifact]:
    if io.iotype not in LINEAGE_VALUES:
        return None

    if io.iotype == IMAGE:
        image = io.value
        connection = connection_by_names.get(io.connection)
        if connection and connection.schema and connection.schema.url:
            image = "{}/{}".format(connection.schema.url, image)
        return V1RunArtifact(
            name=io.name,
            kind=V1ArtifactKind.DOCKER_IMAGE,
            connection=io.connection,
            summary={"image": image},
            is_input=is_input,
        )


def collect_artifacts_from_io_section(
    io_section: List[V1IO],
    connection_by_names: Dict[str, V1ConnectionType],
    is_input: bool,
) -> List[V1RunArtifact]:
    io_section = to_list(io_section, check_none=True)
    artifacts = [
        collect_artifacts_from_io(
            io, connection_by_names=connection_by_names, is_input=is_input
        )
        for io in io_section
    ]
    return [a for a in artifacts if a]


def collect_io_artifacts(
    compiled_operation: V1CompiledOperation,
    connection_by_names: Dict[str, V1ConnectionType],
) -> List[V1RunArtifact]:
    connection_by_names = connection_by_names or {}
    artifacts = []
    artifacts += collect_artifacts_from_io_section(
        compiled_operation.inputs,
        connection_by_names=connection_by_names,
        is_input=True,
    )
    artifacts += collect_artifacts_from_io_section(
        compiled_operation.outputs,
        connection_by_names=connection_by_names,
        is_input=False,
    )
    return artifacts
