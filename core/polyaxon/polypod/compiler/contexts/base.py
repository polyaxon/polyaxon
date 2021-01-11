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

from polyaxon.polyflow import V1CompiledOperation, V1Init
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.list_utils import to_list


class BaseContextsManager:
    @classmethod
    def _resolve_init_contexts(
        cls,
        contexts: Dict,
        init: List[V1Init],
        connection_by_names: Dict[str, V1ConnectionType],
    ):
        init = to_list(init, check_none=True)
        connections = [i.connection for i in init if i.connection]
        return cls._resolve_connections_contexts(
            contexts=contexts,
            connections=connections,
            connection_by_names=connection_by_names,
            key="init",
        )

    @staticmethod
    def _resolve_connections_contexts(
        contexts: Dict,
        connections: List[str],
        connection_by_names: Dict[str, V1ConnectionType],
        key: str = "connections",
    ) -> Dict:
        connections = to_list(connections, check_none=True)
        for connection in connections:
            if connection_by_names[connection].schema:
                contexts[key][connection] = connection_by_names[
                    connection
                ].schema.to_dict()
        return contexts

    @classmethod
    def _resolver_replica(
        cls,
        contexts: Dict,
        init: List[V1Init],
        connections: List[str],
        connection_by_names: Dict[str, V1ConnectionType],
    ) -> Dict:
        contexts["init"] = {}
        contexts["connections"] = {}
        contexts = cls._resolve_init_contexts(
            contexts=contexts, init=init, connection_by_names=connection_by_names
        )
        contexts = cls._resolve_connections_contexts(
            contexts=contexts,
            connections=connections,
            connection_by_names=connection_by_names,
        )
        return contexts

    @classmethod
    def resolve(
        cls,
        namespace: str,
        owner_name: str,
        project_name: str,
        run_uuid: str,
        contexts: Dict,
        compiled_operation: V1CompiledOperation,
        connection_by_names: Dict[str, V1ConnectionType],
    ) -> Dict:
        raise NotImplementedError()
