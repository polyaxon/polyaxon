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

import pytest

from tests.utils import BaseTestCase

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import V1ClaimConnection
from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyflow import V1CompiledOperation, V1RunKind
from polyaxon.polypod.contexts import resolve_contexts
from polyaxon.schemas.types import V1ConnectionType


@pytest.mark.polypod_mark
class TestResolveContexts(BaseTestCase):
    def test_resolver_default_contexts(self):
        compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": False,
                    "collectResources": False,
                },
                "run": {"kind": V1RunKind.JOB, "container": {"image": "test"},},
            }
        )
        spec = resolve_contexts(
            namespace="test",
            owner_name="user",
            project_name="project",
            project_uuid="uuid",
            run_uuid="uuid",
            run_name="run",
            run_path="test",
            compiled_operation=compiled_operation,
            artifacts_store=None,
            connection_by_names={},
            iteration=None,
        )
        assert spec == {
            "globals": {
                "owner_name": "user",
                "project_unique_name": "user.project",
                "project_name": "project",
                "project_uuid": "uuid",
                "run_info": "user.project.runs.uuid",
                "context_path": "/plx-context",
                "artifacts_path": "/plx-context/artifacts",
                "name": "run",
                "uuid": "uuid",
                "namespace": "test",
                "iteration": None,
            },
            "init": {},
            "connections": {},
        }

    def test_resolver_init_and_connections_contexts(self):
        store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/claim/path", volume_claim="claim", read_only=True
            ),
        )

        compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": False,
                    "collectResources": False,
                },
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"image": "test"},
                    "connections": [store.name],
                    "init": [{"connection": store.name}],
                },
            }
        )
        spec = resolve_contexts(
            namespace="test",
            owner_name="user",
            project_name="project",
            project_uuid="uuid",
            run_uuid="uuid",
            run_name="run",
            run_path="test",
            compiled_operation=compiled_operation,
            artifacts_store=store,
            connection_by_names={store.name: store},
            iteration=12,
        )
        assert spec == {
            "globals": {
                "owner_name": "user",
                "project_unique_name": "user.project",
                "project_name": "project",
                "project_uuid": "uuid",
                "name": "run",
                "uuid": "uuid",
                "context_path": "/plx-context",
                "artifacts_path": "/plx-context/artifacts",
                "run_artifacts_path": "/claim/path/test",
                "run_outputs_path": "/claim/path/test/outputs",
                "namespace": "test",
                "iteration": 12,
                "run_info": "user.project.runs.uuid",
            },
            "init": {"test_claim": store.schema.to_dict()},
            "connections": {"test_claim": store.schema.to_dict()},
        }

    def test_resolver_outputs_collections(self):
        store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/claim/path", volume_claim="claim", read_only=True
            ),
        )
        compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": True,
                    "collectResources": True,
                },
                "run": {
                    "kind": V1RunKind.JOB,
                    "container": {"image": "test"},
                    "connections": [store.name],
                    "init": [{"connection": store.name}],
                },
            }
        )
        spec = resolve_contexts(
            namespace="test",
            owner_name="user",
            project_name="project",
            project_uuid="uuid",
            run_uuid="uuid",
            run_name="run",
            run_path="test",
            compiled_operation=compiled_operation,
            artifacts_store=store,
            connection_by_names={store.name: store},
            iteration=12,
        )
        assert spec == {
            "globals": {
                "owner_name": "user",
                "project_name": "project",
                "project_unique_name": "user.project",
                "project_uuid": "uuid",
                "name": "run",
                "uuid": "uuid",
                "run_info": "user.project.runs.uuid",
                "context_path": "/plx-context",
                "artifacts_path": "/plx-context/artifacts/test",
                "artifacts_path": "/plx-context/artifacts",
                "run_artifacts_path": "/plx-context/artifacts/test",
                "run_outputs_path": "/plx-context/artifacts/test/outputs",
                "namespace": "test",
                "iteration": 12,
            },
            "init": {"test_claim": store.schema.to_dict()},
            "connections": {"test_claim": store.schema.to_dict()},
        }

    def test_resolver_default_service_ports(self):
        compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": True,
                    "collectResources": True,
                },
                "run": {
                    "kind": V1RunKind.SERVICE,
                    "ports": [1212, 1234],
                    "container": {"image": "test", "command": "{{ ports[0] }}"},
                },
            }
        )
        spec = resolve_contexts(
            namespace="test",
            owner_name="user",
            project_name="project",
            project_uuid="uuid",
            run_uuid="uuid",
            run_name="run",
            run_path="test",
            compiled_operation=compiled_operation,
            artifacts_store=None,
            connection_by_names={},
            iteration=12,
        )
        assert spec == {
            "globals": {
                "owner_name": "user",
                "project_name": "project",
                "project_unique_name": "user.project",
                "project_uuid": "uuid",
                "run_info": "user.project.runs.uuid",
                "name": "run",
                "uuid": "uuid",
                "context_path": "/plx-context",
                "artifacts_path": "/plx-context/artifacts",
                "run_artifacts_path": "/plx-context/artifacts/test",
                "run_outputs_path": "/plx-context/artifacts/test/outputs",
                "namespace": "test",
                "iteration": 12,
                "ports": [1212, 1234],
                "base_url": "/services/v1/test/user/project/runs/uuid",
            },
            "init": {},
            "connections": {},
        }
