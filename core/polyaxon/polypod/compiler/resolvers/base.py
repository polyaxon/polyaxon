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
from polyaxon.polyaxonfile import CompiledOperationSpecification
from polyaxon.polyflow import V1CompiledOperation
from polyaxon.polypod.compiler.config import PolypodConfig
from polyaxon.polypod.contexts import resolve_contexts, resolve_globals_contexts


class BaseResolver:
    KINDS = set()

    def __init__(
        self,
        run,
        compiled_operation: V1CompiledOperation,
        owner_name: str,
        project_name: str,
        project_uuid: str,
        run_name: str,
        run_uuid: str,
        run_path: str,
        params: Optional[Dict],
    ):
        if not compiled_operation:
            raise PolyaxonCompilerError("A run spec is required for resolution.")
        self.run = run
        self.compiled_operation = compiled_operation
        self.owner_name = owner_name
        self.project_name = project_name
        self.project_uuid = project_uuid
        self.run_name = run_name
        self.run_uuid = run_uuid
        self.run_path = run_path
        self.params = params or {}
        self.connection_by_names = {}
        self.namespace = None
        self.artifacts_store = None
        self.secrets = None
        self.config_maps = None
        self.polyaxon_sidecar = None
        self.polyaxon_init = None
        self.iteration = None
        self.agent_config = None
        self.contexts = {}
        self.globals = {}

    def resolve_edges(self):
        pass

    def resolve_globals(self):
        self.globals = resolve_globals_contexts(
            namespace=self.namespace,
            owner_name=self.owner_name,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            run_name=self.run_name,
            run_path=self.run_path,
            run_uuid=self.run_uuid,
            iteration=self.iteration,
        )

    def resolve_params(self):
        raise NotImplementedError

    def resolve_connections_params(self):
        self.compiled_operation = CompiledOperationSpecification.apply_run_connections_params(
            config=self.compiled_operation,
            artifact_store=self.artifacts_store.name if self.artifacts_store else None,
            contexts=self.globals,
        )

    def resolve_profile(self):
        pass

    def resolve_agent(self):
        pass

    def patch(self):
        pass

    def apply_content(self):
        try:
            self.compiled_operation = CompiledOperationSpecification.apply_context(
                self.compiled_operation
            )
        except Exception as e:
            raise PolyaxonCompilerError(
                "Could not apply run context, error: {}".format(repr(e))
            )

    def resolve_io(self):
        pass

    def resolve_access(self):
        pass

    def resolve_connections(self):
        polypod_config = PolypodConfig()
        polypod_config.resolve(
            compiled_operation=self.compiled_operation, agent_config=self.agent_config
        )
        self.polyaxon_sidecar = polypod_config.polyaxon_sidecar
        self.polyaxon_init = polypod_config.polyaxon_init
        self.namespace = polypod_config.namespace
        self.secrets = polypod_config.secrets
        self.config_maps = polypod_config.config_maps
        self.connection_by_names = polypod_config.connection_by_names
        self.artifacts_store = polypod_config.artifacts_store

    def resolve_contexts(self):
        self.contexts = resolve_contexts(
            namespace=self.namespace,
            owner_name=self.owner_name,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            run_name=self.run_name,
            run_path=self.run_path,
            run_uuid=self.run_uuid,
            compiled_operation=self.compiled_operation,
            connection_by_names=self.connection_by_names,
            artifacts_store=self.artifacts_store,
            iteration=self.iteration,
        )

    def apply_contexts(self):
        self.compiled_operation = CompiledOperationSpecification.apply_run_contexts(
            self.compiled_operation, contexts=self.contexts
        )

    def resolve_state(self):
        pass

    def resolve(self) -> V1CompiledOperation:
        self.resolve_edges()
        self.resolve_globals()
        self.resolve_params()
        self.resolve_profile()
        self.resolve_agent()
        self.resolve_connections_params()
        self.patch()
        self.apply_content()
        self.resolve_io()
        self.resolve_access()
        self.resolve_connections()
        self.resolve_contexts()
        self.apply_contexts()
        self.resolve_state()
        return self.compiled_operation
