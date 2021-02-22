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
from typing import List

from polyaxon import settings
from polyaxon.auxiliaries import (
    get_default_init_container,
    get_default_sidecar_container,
)
from polyaxon.exceptions import PolyaxonCompilerError
from polyaxon.polyflow import V1CompiledOperation, V1Init
from polyaxon.schemas.cli.agent_config import AgentConfig
from polyaxon.utils.list_utils import to_list


class PolypodConfig:
    def __init__(self, internal_auth: bool = False):
        self.polyaxon_sidecar = None
        self.polyaxon_init = None
        self.namespace = None
        self.secrets = None
        self.config_maps = None
        self.connection_by_names = {}
        self.artifacts_store = None
        self.default_sa = None
        self.internal_auth = internal_auth

    def resolve(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig = None
    ):
        if not agent_config and settings.AGENT_CONFIG:
            agent_config = settings.AGENT_CONFIG.clone()
        if not agent_config:
            raise PolyaxonCompilerError(
                "Polypod configuration not found or agent not configured."
            )

        self.default_sa = agent_config.runs_sa
        self._resolve_run_connections(
            compiled_operation=compiled_operation, agent_config=agent_config
        )
        self.artifacts_store = agent_config.artifacts_store

        self.secrets = agent_config.secrets
        self.config_maps = agent_config.config_maps

        self.polyaxon_sidecar = agent_config.sidecar or get_default_sidecar_container()
        self.polyaxon_init = agent_config.init or get_default_init_container()
        self.namespace = agent_config.namespace
        self.polyaxon_sidecar.monitor_logs = agent_config.is_replica

    def _resolve_run_connections(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig
    ):
        if agent_config.artifacts_store:  # Resolve default artifacts store
            self.connection_by_names[
                agent_config.artifacts_store.name
            ] = agent_config.artifacts_store

        if compiled_operation.is_job_run or compiled_operation.is_service_run:
            self._resolve_replica_connections(
                init=compiled_operation.run.init,
                connections=compiled_operation.run.connections,
                agent_config=agent_config,
            )
        if compiled_operation.is_distributed_run:
            self._resolve_distributed_connections(
                compiled_operation=compiled_operation, agent_config=agent_config
            )
        if compiled_operation.is_dag_run:
            self._resolve_connections(
                connections=compiled_operation.run.connections,
                agent_config=agent_config,
            )
        if compiled_operation.is_notifier_run:
            self._resolve_notification_connections(
                connections=compiled_operation.run.connections,
                agent_config=agent_config,
            )

    def _resolve_connections(self, connections: List[str], agent_config: AgentConfig):
        if connections:
            connection_by_names = {}
            missing_connections = set()
            for c in connections:
                if c not in agent_config.connections_by_names:
                    missing_connections.add(c)
                else:
                    connection_by_names[c] = agent_config.connections_by_names[c]
            if missing_connections:
                raise PolyaxonCompilerError(
                    "Some Connection refs were provided "
                    "but were not found in the "
                    "agent.connections catalog: `{}`".format(missing_connections)
                )
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
        self, connections: List[str], init: List[V1Init], agent_config: AgentConfig
    ):
        connections = to_list(connections, check_none=True)
        self._resolve_connections(connections=connections, agent_config=agent_config)
        init = to_list(init, check_none=True)
        init = [i.connection for i in init if i.connection]
        self._resolve_connections(connections=init, agent_config=agent_config)

    def _resolve_distributed_connections(
        self, compiled_operation: V1CompiledOperation, agent_config: AgentConfig
    ):
        def _resolve_replica(replica):
            if not replica:
                return
            self._resolve_replica_connections(
                init=replica.init,
                connections=replica.connections,
                agent_config=agent_config,
            )

        if compiled_operation.is_mpi_job_run:
            _resolve_replica(compiled_operation.run.launcher)
            _resolve_replica(compiled_operation.run.worker)
        if compiled_operation.is_tf_job_run:
            _resolve_replica(compiled_operation.run.chief)
            _resolve_replica(compiled_operation.run.worker)
            _resolve_replica(compiled_operation.run.ps)
            _resolve_replica(compiled_operation.run.evaluator)
        if compiled_operation.is_pytorch_job_run:
            _resolve_replica(compiled_operation.run.master)
            _resolve_replica(compiled_operation.run.worker)
