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
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.env_vars.keys import POLYAXON_KEYS_LOG_LEVEL
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow import V1Init, V1Plugins
from polyaxon.polypod.common.env_vars import get_env_var
from polyaxon.polypod.common.mounts import (
    get_artifacts_context_mount,
    get_auth_context_mount,
    get_mounts,
)
from polyaxon.polypod.main.container import MAIN_JOB_CONTAINER, get_main_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


@pytest.mark.polypod_mark
class TestMainContainer(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Secrets and config maps
        self.non_mount_resource1 = V1K8sResourceType(
            name="non_mount_test1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=False,
        )
        self.request_non_mount_resource1 = V1K8sResourceType(
            name="request_non_mount_resource1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=True,
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
        self.request_mount_resource2 = V1K8sResourceType(
            name="mount_test1",
            schema=V1K8sResourceSchema(name="ref", mount_path="/tmp2"),
            is_requested=True,
        )
        # Connections
        self.gcs_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=self.mount_resource1.schema,
        )
        self.s3_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
            secret=self.non_mount_resource1.schema,
        )
        self.az_store = V1ConnectionType(
            name="test_az",
            kind=V1ConnectionKind.WASB,
            schema=V1BucketConnection(bucket="wasb://x@y.blob.core.windows.net"),
            secret=self.non_mount_resource1.schema,
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

    def assert_artifacts_store_raises(self, store, run_path):
        with self.assertRaises(PolypodException):
            get_main_container(
                main_container=None,
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(collect_artifacts=True, collect_logs=False)
                ),
                volume_mounts=None,
                log_level=None,
                artifacts_store=store,
                init=None,
                connection_by_names=None,
                connections=None,
                secrets=None,
                config_maps=None,
                kv_env_vars=None,
                env=None,
                ports=None,
                run_path=run_path,
            )

    def test_get_main_container_with_artifacts_store_with_wrong_paths_raises(self):
        artifacts_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        self.assert_artifacts_store_raises(store=artifacts_store, run_path=None)

        artifacts_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        self.assert_artifacts_store_raises(store=artifacts_store, run_path=[])

    def test_get_main_container_with_none_values(self):
        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=None,
            volume_mounts=None,
            log_level=None,
            artifacts_store=None,
            init=None,
            connection_by_names=None,
            connections=None,
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path=None,
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert container.env == []
        assert container.env_from == []
        assert container.resources is None
        assert container.volume_mounts == []

    def test_get_main_container_simple_params(self):
        initial_mounts = [
            k8s_schemas.V1VolumeMount(
                name="test", mount_path="/mount_test", read_only=True
            )
        ]
        resources = k8s_schemas.V1ResourceRequirements(
            requests={"cpu": "1", "memory": "256Mi"},
            limits={"cpu": "1", "memory": "256Mi"},
        )
        container = get_main_container(
            main_container=k8s_schemas.V1Container(
                name="main",
                image="job_docker_image",
                image_pull_policy="IfNotPresent",
                command=["cmd", "-p", "-c"],
                args=["arg1", "arg2"],
                resources=resources,
            ),
            contexts=None,
            volume_mounts=initial_mounts,
            log_level="info",
            artifacts_store=None,
            init=None,
            connection_by_names=None,
            connections=None,
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=23,
            run_path=None,
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image == "job_docker_image"
        assert container.image_pull_policy == "IfNotPresent"
        assert container.command == ["cmd", "-p", "-c"]
        assert container.args == ["arg1", "arg2"]
        assert container.ports == [k8s_schemas.V1ContainerPort(container_port=23)]
        assert container.env == [
            get_env_var(name=POLYAXON_KEYS_LOG_LEVEL, value="info")
        ]
        assert container.env_from == []
        assert container.resources == resources
        assert container.volume_mounts == initial_mounts

    def test_get_main_container_with_mounted_artifacts_store(self):
        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=None,
            volume_mounts=None,
            log_level=None,
            artifacts_store=None,
            init=[V1Init(connection=self.claim_store.name)],
            connections=None,
            connection_by_names={self.claim_store.name: self.claim_store},
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 1

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=None,
            volume_mounts=None,
            log_level=None,
            artifacts_store=None,
            init=[V1Init(connection=self.claim_store.name)],
            connections=[self.claim_store.name],
            connection_by_names={self.claim_store.name: self.claim_store},
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 2

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True, collect_logs=True, collect_resources=True
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.claim_store,
            init=None,
            connections=[],
            connection_by_names={self.claim_store.name: self.claim_store},
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 2
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 1

    def test_get_main_container_with_bucket_artifacts_store(self):
        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True, collect_logs=True, collect_resources=True
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.s3_store,
            init=None,
            connections=None,
            connection_by_names={self.s3_store.name: self.s3_store},
            secrets=None,
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 2
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 1  # mount context

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True,
                    collect_logs=True,
                    collect_resources=True,
                    sync_statuses=True,
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.s3_store,
            init=None,
            connections=None,
            connection_by_names={self.s3_store.name: self.s3_store},
            secrets=[self.mount_resource1],
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 2
        assert container.env_from == []
        assert container.resources is None
        # The mount resource1 is not requested
        assert len(container.volume_mounts) == 1  # one mount resource

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True, collect_logs=True, collect_resources=True
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.s3_store,
            init=None,
            connections=None,
            connection_by_names={self.s3_store.name: self.s3_store},
            secrets=[self.request_mount_resource2],
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 2
        assert container.env_from == []
        assert container.resources is None
        # The mount resource2 is requested
        assert len(container.volume_mounts) == 2  # one mount resource

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True, collect_logs=True, collect_resources=False
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.s3_store,
            init=None,
            connections=None,
            connection_by_names={self.s3_store.name: self.s3_store},
            secrets=[self.non_mount_resource1],
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 1
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 1  # outputs context

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(
                    collect_artifacts=True, collect_logs=True, collect_resources=True
                )
            ),
            volume_mounts=None,
            log_level=None,
            artifacts_store=self.s3_store,
            init=None,
            connections=None,
            connection_by_names={self.s3_store.name: self.s3_store},
            secrets=[self.request_non_mount_resource1],
            config_maps=None,
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        assert len(container.env) == 2 + 2  # 2 + 2 env vars from the secret mount
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 1

    def test_get_main_container(self):
        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=None,
            volume_mounts=None,
            log_level=None,
            artifacts_store=None,
            init=[
                V1Init(connection=self.claim_store.name),
                V1Init(connection=self.s3_store.name),
            ],
            connections=[self.host_path_store.name, self.gcs_store.name],
            connection_by_names={
                self.claim_store.name: self.claim_store,
                self.s3_store.name: self.s3_store,
                self.host_path_store.name: self.host_path_store,
                self.gcs_store.name: self.gcs_store,
            },
            secrets=[self.mount_resource1, self.request_non_mount_resource1],
            config_maps=[self.non_mount_resource1, self.request_mount_resource2],
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.name == MAIN_JOB_CONTAINER
        assert container.image is None
        assert container.image_pull_policy is None
        assert container.command is None
        assert container.args is None
        assert container.ports == []
        # 2 env vars from the secret mount
        # + 2 for the connection (context_path + spec)
        # + 1 for the connection spec (non mount)
        assert len(container.env) == 5
        assert container.env_from == []
        assert container.resources is None
        assert len(container.volume_mounts) == 4

    def test_get_main_container_host_paths(self):
        contexts = PluginsContextsSpec(
            auth=True,
            docker=False,
            shm=False,
            collect_logs=True,
            collect_artifacts=True,
            collect_resources=True,
            auto_resume=True,
            sync_statuses=True,
        )

        volume_mounts = get_mounts(
            use_auth_context=contexts.auth,
            use_artifacts_context=False,
            use_docker_context=contexts.docker,
            use_shm_context=contexts.shm,
        )

        artifacts_store = V1ConnectionType(
            name="plx-outputs",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                mount_path="/tmp/plx/outputs", host_path="/tmp/plx/outputs"
            ),
        )

        container = get_main_container(
            main_container=k8s_schemas.V1Container(name="main"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=True, collect_logs=True)
            ),
            volume_mounts=volume_mounts,
            log_level=None,
            artifacts_store=artifacts_store,
            init=[],
            connections=[],
            connection_by_names={artifacts_store.name: artifacts_store},
            secrets=[],
            config_maps=[],
            kv_env_vars=None,
            env=None,
            ports=None,
            run_path="run_path",
        )

        assert container.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]
