#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.polyflow import V1Init
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.list_utils import to_list


def get_connection_annotations(
    artifacts_store: Optional[V1ConnectionType],
    init_connections: Optional[List[V1Init]],
    connections: List[str],
    connection_by_names: Optional[Dict[str, V1ConnectionType]],
) -> Dict:
    """Resolve all annotations to inject per replica"""
    connections = to_list(connections, check_none=True)
    init_connections = to_list(init_connections, check_none=True)
    connection_by_names = connection_by_names or {}

    requested_connection_names = connections[:]
    for init_connection in init_connections:
        if (
            init_connection.connection
            and init_connection.connection not in requested_connection_names
        ):
            requested_connection_names.append(init_connection.connection)
    if artifacts_store and artifacts_store.name not in requested_connection_names:
        requested_connection_names.append(artifacts_store.name)

    annotations = {}
    for c in requested_connection_names:
        annotations.update(connection_by_names[c].annotations or {})

    return annotations
