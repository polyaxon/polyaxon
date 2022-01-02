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

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.polyflow import V1Init, V1Plugins
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.volumes import (
    get_artifacts_context_volume,
    get_configs_context_volume,
    get_connections_context_volume,
    get_docker_context_volume,
    get_shm_context_volume,
    get_volume,
    get_volume_from_config_map,
    get_volume_from_connection,
    get_volume_from_secret,
)
from polyaxon.polypod.pod.volumes import get_pod_volumes
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestPodVolumes(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Secrets and config maps
        self.non_mount_resource1 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(
                name="non_mount_test1", items=["item1", "item2"]
            ),
            is_requested=False,
        )
        self.non_mount_resource2 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="non_mount_test2"),
            is_requested=False,
        )
        self.mount_resource1 = V1K8sResourceType(
            name="mount_test1",
            schema=V1K8sResourceSchema(
                name="mount_test1", items=["item1", "item2"], mount_path="/tmp1"
            ),
            is_requested=False,
        )
        self.mount_resource2 = V1K8sResourceType(
            name="mount_test1",
            schema=V1K8sResourceSchema(
                name="mount_test1", items=["item1", "item2"], mount_path="/tmp2"
            ),
            is_requested=False,
        )
        # Volumes
        self.vol1 = get_volume(volume="vol1", claim_name="claim1")
        self.vol2 = get_volume(volume="vol2", host_path="/path2")
        self.vol3 = get_volume(volume="vol3")

        # Connections
        self.s3_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=self.mount_resource1.schema,
        )
        self.gcs_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=self.mount_resource1.schema,
        )
        self.az_store = V1ConnectionType(
            name="test_az",
            kind=V1ConnectionKind.WASB,
            secret=self.mount_resource1.schema,
        )
        self.claim_store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/tmp", volume_claim="test", read_only=True
            ),
        )
        self.host_path_store = V1ConnectionType(
            name="test_path",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(mount_path="/tmp", host_path="/tmp"),
        )

    def test_default_volumes(self):
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=None,
                connections=None,
                connection_by_names=None,
                secrets=None,
                config_maps=None,
                volumes=None,
            )
            == []
        )

        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == []
        )

        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=False,
                        shm=False,
                        auth=False,
                        collect_artifacts=False,
                        collect_logs=False,
                    )
                ),
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == []
        )

        assert get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=False,
                    collect_logs=False,
                )
            ),
            artifacts_store=None,
            init_connections=[],
            connections=[],
            connection_by_names={},
            secrets=[],
            config_maps=[],
            volumes=[],
        ) == [
            get_shm_context_volume(),
            get_configs_context_volume(),
            get_docker_context_volume(),
        ]

    def test_auth_context(self):
        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=False,
                        shm=False,
                        auth=True,
                        collect_artifacts=False,
                        collect_logs=False,
                    )
                ),
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == [get_configs_context_volume()]
        )

    def test_docker_context(self):
        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=True,
                        shm=False,
                        auth=False,
                        collect_artifacts=False,
                        collect_logs=False,
                    )
                ),
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == [get_docker_context_volume()]
        )

    def test_shm_context(self):
        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=False,
                        shm=True,
                        auth=False,
                        collect_artifacts=False,
                        collect_logs=False,
                    )
                ),
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == [get_shm_context_volume()]
        )

    def test_passing_volumes(self):
        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=False,
                        shm=False,
                        auth=False,
                        collect_artifacts=False,
                        collect_logs=False,
                    )
                ),
                artifacts_store=None,
                init_connections=[],
                connections=[],
                connection_by_names={},
                secrets=[],
                config_maps=[],
                volumes=[self.vol1, self.vol2, self.vol3],
            )
            == [self.vol1, self.vol2, self.vol3]
        )

    @staticmethod
    def assert_artifacts_store(store, results):
        assert (
            get_pod_volumes(
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(
                        docker=False,
                        shm=False,
                        auth=False,
                        collect_artifacts=True,
                        collect_logs=False,
                    )
                ),
                artifacts_store=store,
                init_connections=[],
                connections=[],
                connection_by_names={store.name: store},
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == results
        )

    def test_artifacts_store(self):
        self.assert_artifacts_store(
            store=self.s3_store,
            results=[
                get_volume_from_secret(secret=self.mount_resource1),
                get_artifacts_context_volume(),
            ],
        )
        self.assert_artifacts_store(
            store=self.gcs_store,
            results=[
                get_volume_from_secret(secret=self.mount_resource1),
                get_artifacts_context_volume(),
            ],
        )
        self.assert_artifacts_store(
            store=self.az_store,
            results=[
                get_volume_from_secret(secret=self.mount_resource1),
                get_artifacts_context_volume(),
            ],
        )
        self.assert_artifacts_store(
            store=self.claim_store,
            results=[
                get_volume_from_connection(connection=self.claim_store),
                get_artifacts_context_volume(),
            ],
        )
        self.assert_artifacts_store(
            store=self.host_path_store,
            results=[
                get_volume_from_connection(connection=self.host_path_store),
                get_artifacts_context_volume(),
            ],
        )

    @staticmethod
    def assert_single_artifacts_store(store, results):
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[],
                connection_by_names={store.name: store},
                connections=[],
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == results
        )

    @staticmethod
    def assert_single_init_artifacts_store(store, results):
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[V1Init(connection=store.name)],
                connection_by_names={store.name: store},
                connections=[],
                secrets=[],
                config_maps=[],
                volumes=[],
            )
            == results
        )

    def test_single_connections(self):
        self.assert_single_artifacts_store(store=self.s3_store, results=[])
        self.assert_single_artifacts_store(store=self.gcs_store, results=[])
        self.assert_single_artifacts_store(store=self.az_store, results=[])
        self.assert_single_artifacts_store(
            store=self.claim_store,
            results=[get_volume_from_connection(connection=self.claim_store)],
        )
        self.assert_single_artifacts_store(
            store=self.host_path_store,
            results=[get_volume_from_connection(connection=self.host_path_store)],
        )

        # Managed versions
        ctx_volume_name = constants.CONTEXT_VOLUME_ARTIFACTS
        self.assert_single_init_artifacts_store(
            store=self.s3_store,
            results=[
                get_connections_context_volume(name=ctx_volume_name),
                get_volume_from_secret(secret=self.mount_resource1),
            ],
        )
        self.assert_single_init_artifacts_store(
            store=self.gcs_store,
            results=[
                get_connections_context_volume(name=ctx_volume_name),
                get_volume_from_secret(secret=self.mount_resource1),
            ],
        )
        self.assert_single_init_artifacts_store(
            store=self.az_store,
            results=[
                get_connections_context_volume(name=ctx_volume_name),
                get_volume_from_secret(secret=self.mount_resource1),
            ],
        )
        self.assert_single_init_artifacts_store(
            store=self.claim_store,
            results=[
                get_connections_context_volume(name=ctx_volume_name),
                get_volume_from_connection(connection=self.claim_store),
            ],
        )
        self.assert_single_init_artifacts_store(
            store=self.host_path_store,
            results=[
                get_connections_context_volume(name=ctx_volume_name),
                get_volume_from_connection(connection=self.host_path_store),
            ],
        )

    def test_multi_connections(self):
        connection_by_names = {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
            self.az_store.name: self.az_store,
            self.claim_store.name: self.claim_store,
            self.host_path_store.name: self.host_path_store,
        }
        init_connections = [
            V1Init(connection=self.s3_store.name, path="/test-1"),
            V1Init(connection=self.gcs_store.name, path="/test-2"),
            V1Init(connection=self.az_store.name, path="/test-3"),
            V1Init(connection=self.claim_store.name, path="/test-4"),
            V1Init(connection=self.host_path_store.name, path="/test-5"),
        ]
        assert (
            len(
                get_pod_volumes(
                    contexts=None,
                    artifacts_store=None,
                    init_connections=[],
                    connection_by_names=connection_by_names,
                    connections=[],
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 2
        )

        # test all inits are mounted to the same context and a single secret requested for all
        assert (
            len(
                get_pod_volumes(
                    contexts=None,
                    artifacts_store=None,
                    init_connections=[
                        V1Init(connection=self.s3_store.name),
                        V1Init(connection=self.gcs_store.name),
                        V1Init(connection=self.az_store.name),
                        V1Init(connection=self.claim_store.name),
                        V1Init(connection=self.host_path_store.name),
                    ],
                    connection_by_names=connection_by_names,
                    connections=[],
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 4
        )

        assert (
            len(
                get_pod_volumes(
                    contexts=None,
                    artifacts_store=None,
                    init_connections=init_connections,
                    connection_by_names=connection_by_names,
                    connections=[],
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 8
        )

        assert (
            len(
                get_pod_volumes(
                    contexts=None,
                    artifacts_store=None,
                    init_connections=init_connections,
                    connection_by_names=connection_by_names,
                    connections=[],
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 8
        )

        assert (
            len(
                get_pod_volumes(
                    contexts=PluginsContextsSpec.from_config(
                        V1Plugins(
                            docker=True,
                            shm=True,
                            auth=True,
                            collect_artifacts=True,
                            collect_logs=True,
                        )
                    ),
                    artifacts_store=self.claim_store,
                    init_connections=init_connections,
                    connection_by_names=connection_by_names,
                    connections=[],
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 12
        )

        assert (
            len(
                get_pod_volumes(
                    contexts=PluginsContextsSpec.from_config(
                        V1Plugins(
                            docker=True,
                            shm=True,
                            auth=True,
                            collect_artifacts=True,
                            collect_logs=True,
                        )
                    ),
                    artifacts_store=self.claim_store,
                    init_connections=init_connections,
                    connection_by_names=connection_by_names,
                    connections=list(connection_by_names.keys()),
                    secrets=[],
                    config_maps=[],
                    volumes=[],
                )
            )
            == 12
        )

    @staticmethod
    def assert_secret(secret, connection, results):
        dummy_connection = (
            V1ConnectionType(
                name="connection",
                kind=V1ConnectionKind.S3,
                schema=None,
                secret=secret.schema,
            )
            if connection
            else None
        )
        connection_by_names = {"connection": dummy_connection} if connection else {}
        connections = ["connection"] if connection else []
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[],
                connections=connections,
                connection_by_names=connection_by_names,
                secrets=[secret],
                config_maps=[],
                volumes=[],
            )
            == results
        )

    @staticmethod
    def assert_config_map(config_map, connection, results):
        dummy_connection = (
            V1ConnectionType(
                name="connection",
                kind=V1ConnectionKind.S3,
                schema=None,
                config_map=config_map.schema,
            )
            if connection
            else None
        )
        connection_by_names = {"connection": dummy_connection} if connection else {}
        connections = ["connection"] if connection else []
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[],
                connections=connections,
                connection_by_names=connection_by_names,
                secrets=[],
                config_maps=[config_map],
                volumes=[],
            )
            == results
        )

    def test_secret_volumes(self):
        self.assert_secret(
            secret=self.non_mount_resource1, connection=False, results=[]
        )
        self.assert_secret(
            secret=self.non_mount_resource2, connection=False, results=[]
        )
        self.assert_secret(secret=self.mount_resource1, connection=False, results=[])
        self.assert_secret(secret=self.mount_resource2, connection=False, results=[])
        self.assert_secret(
            secret=self.mount_resource1,
            connection=True,
            results=[get_volume_from_secret(secret=self.mount_resource1)],
        )
        self.assert_secret(
            secret=self.mount_resource2,
            connection=True,
            results=[get_volume_from_secret(secret=self.mount_resource2)],
        )

    def test_config_map_volumes(self):
        self.assert_config_map(
            config_map=self.non_mount_resource1, connection=False, results=[]
        )
        self.assert_config_map(
            config_map=self.non_mount_resource2, connection=False, results=[]
        )
        self.assert_config_map(
            config_map=self.mount_resource1, connection=False, results=[]
        )
        self.assert_config_map(
            config_map=self.mount_resource2, connection=False, results=[]
        )
        self.assert_config_map(
            config_map=self.mount_resource1,
            connection=True,
            results=[get_volume_from_config_map(config_map=self.mount_resource1)],
        )
        self.assert_config_map(
            config_map=self.mount_resource2,
            connection=True,
            results=[get_volume_from_config_map(config_map=self.mount_resource2)],
        )

    def test_multiple_resources(self):
        assert (
            get_pod_volumes(
                contexts=None,
                artifacts_store=None,
                init_connections=[],
                connection_by_names={},
                connections=[],
                secrets=[
                    self.non_mount_resource1,
                    self.non_mount_resource1,
                    self.mount_resource1,
                    self.mount_resource2,
                ],
                config_maps=[
                    self.non_mount_resource1,
                    self.non_mount_resource1,
                    self.mount_resource1,
                    self.mount_resource2,
                ],
                volumes=[],
            )
            == []
        )

        # Make the resources requested
        self.non_mount_resource1.is_requested = True
        self.non_mount_resource2.is_requested = True
        self.mount_resource1.is_requested = True
        self.mount_resource2.is_requested = True
        assert get_pod_volumes(
            contexts=None,
            artifacts_store=None,
            init_connections=[],
            connection_by_names={},
            connections=[],
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource2,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource2,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[],
        ) == [
            get_volume_from_secret(secret=self.mount_resource1),
            get_volume_from_secret(secret=self.mount_resource2),
            get_volume_from_config_map(config_map=self.mount_resource1),
            get_volume_from_config_map(config_map=self.mount_resource2),
        ]

    def test_all_volumes_and_init_in_the_same_context(self):
        connection_by_names = {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
            self.az_store.name: self.az_store,
            self.claim_store.name: self.claim_store,
            self.host_path_store.name: self.host_path_store,
        }

        # Test all init are in the same context
        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=[
                V1Init(connection=self.s3_store.name),
                V1Init(connection=self.gcs_store.name),
                V1Init(connection=self.az_store.name),
                V1Init(connection=self.claim_store.name),
                V1Init(connection=self.host_path_store.name),
            ],
            connections=[],
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume) / 1 managed contexts
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 2 mount volumes
        # 1: 1 mount secret
        assert len(pod_volumes) == 1 + 3 + 3 + 2 + 1

        # Test all init are in the same context
        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=[
                V1Init(connection=self.s3_store.name),
                V1Init(connection=self.gcs_store.name),
                V1Init(connection=self.az_store.name),
                V1Init(connection=self.claim_store.name),
                V1Init(connection=self.host_path_store.name),
            ],
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume) / 1 managed contexts
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 2 mount volumes
        # 4: 1 mount resources (secrets + configs)
        assert len(pod_volumes) == 1 + 3 + 3 + 2 + 1

        # Enable requesting resources
        self.mount_resource1.is_requested = True
        self.mount_resource2.is_requested = True
        # Test all init are in the same context and requested values
        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=[
                V1Init(connection=self.s3_store.name),
                V1Init(connection=self.gcs_store.name),
                V1Init(connection=self.az_store.name),
                V1Init(connection=self.claim_store.name),
                V1Init(connection=self.host_path_store.name),
            ],
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume) / 1 managed contexts
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 2 mount volumes
        # 4: 4 mount resources (secrets + configs)
        assert len(pod_volumes) == 1 + 3 + 3 + 2 + 4

    def test_all_volumes(self):
        connection_by_names = {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
            self.az_store.name: self.az_store,
            self.claim_store.name: self.claim_store,
            self.host_path_store.name: self.host_path_store,
        }

        init_connections = [
            V1Init(connection=self.s3_store.name, path="/test-1"),
            V1Init(connection=self.gcs_store.name, path="/test-2"),
            V1Init(connection=self.az_store.name, path="/test-3"),
            V1Init(connection=self.claim_store.name, path="/test-4"),
            V1Init(connection=self.host_path_store.name, path="/test-5"),
        ]

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            connections=[],
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume)
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 5: 5 managed contexts + 2 mount volumes
        # 1: 1 secret
        assert len(pod_volumes) == 1 + 3 + 3 + 7 + 1

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            connections=list(connection_by_names.keys()),
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume)
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 5 managed contexts + 2 mount volumes
        assert len(pod_volumes) == 1 + 3 + 3 + 7 + 1

        # Enable requesting resources
        self.mount_resource1.is_requested = True
        self.mount_resource2.is_requested = True
        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.claim_store,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            connections=[],
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume)
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 5 managed contexts + 2 mount volumes
        # 4: 4 mount resources (secrets + configs)
        assert len(pod_volumes) == 1 + 3 + 3 + 7 + 4

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.s3_store,
            init_connections=init_connections,
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 1: logs/output contexts (same volume)
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 5 managed contexts + 2 mount volumes
        # 4: 4 mount resources (secrets + configs)
        assert len(pod_volumes) == 1 + 3 + 3 + 7 + 4

    def test_all_volumes_and_artifacts_store(self):
        connection_by_names = {
            self.s3_store.name: self.s3_store,
            self.gcs_store.name: self.gcs_store,
            self.az_store.name: self.az_store,
            self.claim_store.name: self.claim_store,
            self.host_path_store.name: self.host_path_store,
        }

        init_connections = [
            V1Init(connection=self.s3_store.name, path="/test-1"),
            V1Init(connection=self.gcs_store.name, path="/test-2"),
            V1Init(connection=self.az_store.name, path="/test-3"),
            V1Init(connection=self.claim_store.name, path="/test-4"),
            V1Init(connection=self.host_path_store.name, path="/test-5"),
        ]

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=False,
                    collect_logs=False,
                )
            ),
            artifacts_store=None,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            connections=[],
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 5: 5 managed contexts + 2 mount volumes
        # 1: 1 secret
        assert len(pod_volumes) == 3 + 3 + 7 + 1

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=False,
                    collect_logs=False,
                )
            ),
            artifacts_store=None,
            init_connections=init_connections,
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 3: 3 context requested constant contexts
        # 3: 3 volumes
        # 7: 5 managed contexts + 2 mount volumes
        assert len(pod_volumes) == 3 + 3 + 7 + 1

        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.host_path_store,
            init_connections=[
                V1Init(connection=self.s3_store.name),
                V1Init(connection=self.gcs_store.name),
                V1Init(connection=self.az_store.name),
            ],
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 4: 4 context requested constant contexts / init volumes contexts
        # 3: 3 volumes
        # 2: 2 managed volumes
        assert len(pod_volumes) == 4 + 2 + 3 + 1

        # Enable requesting resources
        self.mount_resource1.is_requested = True
        self.mount_resource2.is_requested = True
        pod_volumes = get_pod_volumes(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    docker=True,
                    shm=True,
                    auth=True,
                    collect_artifacts=True,
                    collect_logs=True,
                )
            ),
            artifacts_store=self.host_path_store,
            init_connections=[
                V1Init(connection=self.s3_store.name),
                V1Init(connection=self.gcs_store.name),
                V1Init(connection=self.az_store.name),
            ],
            connections=list(connection_by_names.keys()),
            connection_by_names=connection_by_names,
            secrets=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            config_maps=[
                self.non_mount_resource1,
                self.non_mount_resource1,
                self.mount_resource1,
                self.mount_resource2,
            ],
            volumes=[self.vol1, self.vol2, self.vol3],
        )
        # 4: 4 context requested constant contexts / init volumes contexts
        # 3: 3 volumes
        # 2: 2 managed volumes
        # 4: 4 mount resources (secrets + configs)
        assert len(pod_volumes) == 4 + 2 + 3 + 4
