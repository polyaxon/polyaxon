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

import pytest
import tempfile

from polyaxon import settings, types
from polyaxon.auxiliaries import (
    get_default_init_container,
    get_default_sidecar_container,
)
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1HostConnection,
    V1K8sResourceSchema,
)
from polyaxon.managers.agent import AgentConfigManager
from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyflow import V1CompiledOperation, V1RunKind
from polyaxon.polypod.compiler.lineage.io_collector import collect_io_artifacts
from polyaxon.polypod.compiler.resolver import BaseResolver
from polyaxon.schemas.cli.agent_config import AgentConfig
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestLineageResolver(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.compiled_operation = V1CompiledOperation.read(
            {
                "version": 1.1,
                "kind": kinds.COMPILED_OPERATION,
                "inputs": [
                    {
                        "name": "param1",
                        "type": types.STR,
                        "value": "test",
                        "isOptional": "true",
                    },
                    {
                        "name": "param1",
                        "type": types.IMAGE,
                        "isOptional": "true",
                        "value": "repo1",
                        "connection": "connection1",
                    },
                    {
                        "name": "param1",
                        "type": types.IMAGE,
                        "isOptional": "true",
                        "value": "repo2",
                        "connection": "connection2",
                    },
                ],
                "outputs": [
                    {
                        "name": "repo2",
                        "type": types.IMAGE,
                        "isOptional": "true",
                        "value": "repo3",
                        "connection": "connection1",
                    }
                ],
                "run": {
                    "kind": V1RunKind.JOB,
                    "connections": {"test_s3", "connection1", "connection2"},
                    "container": {"image": "test"},
                },
            }
        )

    def test_collector_without_connections(self):
        artifacts = collect_io_artifacts(
            compiled_operation=self.compiled_operation, connection_by_names={}
        )
        assert len(artifacts) == 3
        assert {a.is_input for a in artifacts} == {True, False}
        assert {a.kind for a in artifacts} == {V1ArtifactKind.DOCKER_IMAGE}
        assert {a.connection for a in artifacts} == {"connection1", "connection2"}
        assert {a.summary.get("image") for a in artifacts} == {
            "repo1",
            "repo2",
            "repo3",
        }

    def test_collector_with_connections(self):
        connection1 = V1ConnectionType(
            name="connection1",
            kind=V1ConnectionKind.REGISTRY,
            schema=V1HostConnection(url="localhost:5000"),
            secret="test",
        )
        artifacts = collect_io_artifacts(
            compiled_operation=self.compiled_operation,
            connection_by_names={"connection1": connection1},
        )
        assert len(artifacts) == 3
        assert {a.is_input for a in artifacts} == {True, False}
        assert {a.kind for a in artifacts} == {V1ArtifactKind.DOCKER_IMAGE}
        assert {a.connection for a in artifacts} == {"connection1", "connection2"}
        assert {a.summary.get("image") for a in artifacts} == {
            "localhost:5000/repo1",
            "repo2",
            "localhost:5000/repo3",
        }

    def test_resolve_connections_with_invalid_config(self):
        fpath = tempfile.mkdtemp()
        AgentConfigManager.CONFIG_PATH = fpath
        secret1 = V1K8sResourceType(
            name="secret1",
            schema=V1K8sResourceSchema(name="secret1"),
            is_requested=True,
        )
        secret2 = V1K8sResourceType(
            name="secret2",
            schema=V1K8sResourceSchema(name="secret2"),
            is_requested=True,
        )
        artifacts_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=secret1.schema,
        )
        connection1 = V1ConnectionType(
            name="connection1",
            kind=V1ConnectionKind.REGISTRY,
            schema=V1HostConnection(url="localhost:5000"),
            secret=secret2.schema,
        )
        connection2 = V1ConnectionType(
            name="connection2",
            kind=V1ConnectionKind.REGISTRY,
        )
        settings.AGENT_CONFIG = AgentConfig(
            namespace="foo",
            artifacts_store=artifacts_store,
            connections=[connection1, connection2],
        )

        resolver = BaseResolver(
            run=None,
            compiled_operation=self.compiled_operation,
            owner_name="user",
            project_name="p1",
            project_uuid=None,
            run_name="j1",
            run_uuid=None,
            run_path="test",
            params=None,
        )
        resolver.resolve_connections()
        assert resolver.namespace == "foo"
        assert resolver.connection_by_names == {
            artifacts_store.name: artifacts_store,
            connection1.name: connection1,
            connection2.name: connection2,
        }
        assert resolver.artifacts_store == artifacts_store
        assert resolver.polyaxon_sidecar == get_default_sidecar_container()
        assert resolver.polyaxon_init == get_default_init_container()
        resolver.resolve_artifacts_lineage()
        assert len(resolver.artifacts) == 3
