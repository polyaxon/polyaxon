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

from polyaxon_sdk import V1BucketConnection

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.polyflow import V1Init, V1Plugins
from polyaxon.polypod.common.mounts import (
    get_artifacts_context_mount,
    get_connections_context_mount,
    get_mount_from_resource,
    get_mount_from_store,
)
from polyaxon.polypod.common.volumes import get_volume, get_volume_name
from polyaxon.polypod.main.volumes import get_volume_mounts
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestMainMounts(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Secrets and config maps
        self.non_mount_resource1 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=False,
        )
        self.non_mount_resource2 = V1K8sResourceType(
            name="non_mount_test2",
            schema=V1K8sResourceSchema(name="ref"),
            is_requested=False,
        )
        self.mount_resource1 = V1K8sResourceType(
            name="mount_test1",
            schema=V1K8sResourceSchema(
                name="ref", items=["item1", "item2"], mount_path="/tmp1"
            ),
            is_requested=False,
        )
        self.mount_resource2 = V1K8sResourceType(
            name="mount_test2",
            schema=V1K8sResourceSchema(name="ref", mount_path="/tmp2"),
            is_requested=False,
        )
        # Volumes
        self.vol1 = get_volume(volume="vol1", claim_name="claim1")
        self.vol2 = get_volume(volume="vol2", host_path="/path2")
        self.vol3 = get_volume(volume="vol3")
        # connections
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
            schema=V1BucketConnection(bucket="wasb://x@y.blob.core.windows.net"),
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
            schema=V1HostPathConnection(
                mount_path="/tmp", host_path="/tmp", read_only=True
            ),
        )

    def test_get_volume_mounts(self):
        assert (
            get_volume_mounts(
                contexts=None,
                init=None,
                connections=None,
                secrets=None,
                config_maps=None,
            )
            == []
        )
        assert (
            get_volume_mounts(
                contexts=None, init=[], connections=[], secrets=[], config_maps=[]
            )
            == []
        )

    @staticmethod
    def assert_contexts_store(contexts, results):
        assert (
            get_volume_mounts(
                contexts=contexts, init=[], connections=[], secrets=[], config_maps=[]
            )
            == results
        )

    def test_artifacts_store(self):
        self.assert_contexts_store(contexts=None, results=[])
        self.assert_contexts_store(
            contexts=PluginsContextsSpec.from_config(
                PluginsContextsSpec.from_config(
                    V1Plugins(collect_logs=False, collect_artifacts=True)
                )
            ),
            results=[get_artifacts_context_mount(read_only=False)],
        )
        self.assert_contexts_store(
            contexts=PluginsContextsSpec.from_config(
                PluginsContextsSpec.from_config(
                    V1Plugins(collect_logs=True, collect_artifacts=False)
                )
            ),
            results=[],
        )
        self.assert_contexts_store(
            contexts=PluginsContextsSpec.from_config(
                PluginsContextsSpec.from_config(
                    V1Plugins(collect_logs=True, collect_artifacts=True)
                )
            ),
            results=[get_artifacts_context_mount(read_only=False)],
        )

    @staticmethod
    def assert_single_store(store, results):
        assert (
            get_volume_mounts(
                contexts=None, init=[], connections=[store], secrets=[], config_maps=[]
            )
            == results
        )

    @staticmethod
    def assert_single_init_store(store, results):
        assert (
            get_volume_mounts(
                contexts=None,
                init=[V1Init(connection=store.name, path="/test")],
                connections=[],
                secrets=[],
                config_maps=[],
            )
            == results
        )

    def test_single_connections(self):
        self.assert_single_store(store=self.s3_store, results=[])
        self.assert_single_store(store=self.gcs_store, results=[])
        self.assert_single_store(store=self.az_store, results=[])
        self.assert_single_store(
            store=self.claim_store,
            results=[get_mount_from_store(store=self.claim_store)],
        )
        self.assert_single_store(
            store=self.host_path_store,
            results=[get_mount_from_store(store=self.host_path_store)],
        )

        # Managed versions
        volume_name = get_volume_name("/test")
        self.assert_single_init_store(
            store=self.s3_store,
            results=[
                get_connections_context_mount(name=volume_name, mount_path="/test")
            ],
        )
        self.assert_single_init_store(
            store=self.gcs_store,
            results=[
                get_connections_context_mount(name=volume_name, mount_path="/test")
            ],
        )
        self.assert_single_init_store(
            store=self.az_store,
            results=[
                get_connections_context_mount(name=volume_name, mount_path="/test")
            ],
        )
        self.assert_single_init_store(
            store=self.claim_store,
            results=[
                get_connections_context_mount(name=volume_name, mount_path="/test")
            ],
        )
        self.assert_single_init_store(
            store=self.host_path_store,
            results=[
                get_connections_context_mount(name=volume_name, mount_path="/test")
            ],
        )

    def test_multi_connections(self):
        assert (
            len(
                get_volume_mounts(
                    contexts=None,
                    init=[],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
                    secrets=[],
                    config_maps=[],
                )
            )
            == 2
        )

        assert (
            len(
                get_volume_mounts(
                    contexts=None,
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[],
                    secrets=[],
                    config_maps=[],
                )
            )
            == 5
        )

        assert (
            len(
                get_volume_mounts(
                    contexts=None,
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
                    secrets=[],
                    config_maps=[],
                )
            )
            == 7
        )

    @staticmethod
    def assert_secret(secret, results):
        assert (
            get_volume_mounts(
                contexts=None, init=[], connections=[], secrets=[secret], config_maps=[]
            )
            == results
        )

    @staticmethod
    def assert_config_map(config_map, results):
        assert (
            get_volume_mounts(
                contexts=None,
                init=[],
                connections=[],
                secrets=[],
                config_maps=[config_map],
            )
            == results
        )

    def test_secret_volumes(self):
        self.assert_secret(secret=self.non_mount_resource1, results=[])
        self.assert_secret(secret=self.non_mount_resource2, results=[])
        self.assert_secret(
            secret=self.mount_resource1,
            results=[get_mount_from_resource(resource=self.mount_resource1)],
        )
        self.assert_secret(
            secret=self.mount_resource2,
            results=[get_mount_from_resource(resource=self.mount_resource2)],
        )

    def test_config_map_volumes(self):
        self.assert_config_map(config_map=self.non_mount_resource1, results=[])
        self.assert_config_map(config_map=self.non_mount_resource2, results=[])
        self.assert_config_map(
            config_map=self.mount_resource1,
            results=[get_mount_from_resource(resource=self.mount_resource1)],
        )
        self.assert_config_map(
            config_map=self.mount_resource2,
            results=[get_mount_from_resource(resource=self.mount_resource2)],
        )

    def test_multiple_resources(self):
        assert get_volume_mounts(
            contexts=None,
            init=[],
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
        ) == [
            get_mount_from_resource(resource=self.mount_resource1),
            get_mount_from_resource(resource=self.mount_resource2),
            get_mount_from_resource(resource=self.mount_resource1),
            get_mount_from_resource(resource=self.mount_resource2),
        ]

    def test_all_volumes(self):
        assert (
            len(
                get_volume_mounts(
                    contexts=PluginsContextsSpec.from_config(
                        V1Plugins(collect_logs=False, collect_artifacts=True)
                    ),
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
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
                )
            )
            # 1: output store
            # 7: 5 managed contexts + 2 mounts
            # 4: 4 mount resources (secrets + configs)
            == 1 + 7 + 4
        )
        assert (
            len(
                get_volume_mounts(
                    contexts=None,
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
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
                )
            )
            # 7: 5 managed contexts + 2 mounts
            # 4: 4 mount resources (secrets + configs)
            == 7 + 4
        )

        assert (
            len(
                get_volume_mounts(
                    contexts=PluginsContextsSpec.from_config(
                        V1Plugins(collect_logs=True, collect_artifacts=True)
                    ),
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
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
                )
            )
            # 1: outputs context store
            # 7: 5 managed contexts + 2 mounts
            # 4: 4 mount resources (secrets + configs)
            == 1 + 7 + 4
        )
        assert (
            len(
                get_volume_mounts(
                    contexts=PluginsContextsSpec.from_config(
                        V1Plugins(collect_logs=True, collect_artifacts=False)
                    ),
                    init=[
                        V1Init(connection=self.s3_store.name, path="/test-1"),
                        V1Init(connection=self.gcs_store.name, path="/test-2"),
                        V1Init(connection=self.az_store.name, path="/test-3"),
                        V1Init(connection=self.claim_store.name, path="/test-4"),
                        V1Init(connection=self.host_path_store.name, path="/test-5"),
                    ],
                    connections=[
                        self.s3_store,
                        self.gcs_store,
                        self.az_store,
                        self.claim_store,
                        self.host_path_store,
                    ],
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
                )
            )
            # 7: 5 managed contexts + 2 mounts
            # 4: 4 mount resources (secrets + configs)
            == 7 + 4
        )
