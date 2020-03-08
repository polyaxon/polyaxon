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

from polyaxon import settings
from polyaxon.containers.containers import (
    get_default_init_container,
    get_default_sidecar_container,
)
from polyaxon.exceptions import PolyaxonCompilerError
from polyaxon.polyflow import V1CompiledOperation, V1Init
from polyaxon.schemas.cli.agent_config import AgentConfig


class PolypodConfig:
    def __init__(self, internal_auth: bool = False):
        self.polyaxon_sidecar = None
        self.polyaxon_init = None
        self.namespace = None
        self.secrets = None
        self.config_maps = None
        self.connection_by_names = {}
        self.artifacts_store = None
        self.internal_auth = internal_auth

    def resolve(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig = None
    ):
        agent_config = agent_config or settings.AGENT_CONFIG
        if not agent_config:
            raise PolyaxonCompilerError("Polypod is not configured.")

        self._resolve_run_connections(
            compiled_operation=compiled_operation, agent_config=agent_config
        )
        self.artifacts_store = agent_config.artifacts_store

        self.secrets = agent_config.secrets
        self.config_maps = agent_config.config_maps

        self.polyaxon_sidecar = agent_config.sidecar or get_default_sidecar_container()
        self.polyaxon_init = agent_config.init or get_default_init_container()
        self.namespace = agent_config.namespace

    def _resolve_run_connections(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig
    ):
        if agent_config.artifacts_store:  # Resolve default artifacts store
            self.connection_by_names[
                agent_config.artifacts_store.name
            ] = agent_config.artifacts_store

        if compiled_operation.is_job_run or compiled_operation.is_service_run:
            self._resolve_replica_connections(
                compiled_operation=compiled_operation, agent_config=agent_config
            )
        if compiled_operation.is_dag_run:
            self._resolve_connections(
                connections=compiled_operation.run.connections,
                agent_config=agent_config,
            )
        if compiled_operation.is_notifier:
            self._resolve_notification_connections(
                connections=compiled_operation.run.connections,
                agent_config=agent_config,
            )

    def _get_init_connections(self, init: List[V1Init]):
        init = init or []
        return [i.connection for i in init if i.connection]

    def _resolve_connections(self, connections: List[str], agent_config: AgentConfig):
        if connections:
            connection_by_names = {
                c: agent_config.connections_by_names[c] for c in connections
            }
            self.connection_by_names.update(connection_by_names)

    def _resolve_notification_connections(
        self, connections: List[str], agent_config: AgentConfig
    ):
        if connections:
            connection_by_names = {
                c: agent_config.notification_connections_by_names[c]
                for c in connections
            }
            self.connection_by_names.update(connection_by_names)

    def _resolve_replica_connections(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig
    ):
        self._resolve_connections(
            connections=compiled_operation.run.connections, agent_config=agent_config
        )
        init_connections = self._get_init_connections(compiled_operation.run.init)
        self._resolve_connections(
            connections=init_connections, agent_config=agent_config
        )
