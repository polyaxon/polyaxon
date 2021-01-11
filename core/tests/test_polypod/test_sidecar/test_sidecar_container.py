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

from polyaxon.auxiliaries import V1PolyaxonSidecarContainer, get_sidecar_resources
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.exceptions import PolypodException
from polyaxon.polyflow import V1Plugins
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_from_secret,
    get_env_var,
    get_items_from_secret,
)
from polyaxon.polypod.common.mounts import (
    get_artifacts_context_mount,
    get_auth_context_mount,
    get_mount_from_resource,
    get_mount_from_store,
)
from polyaxon.polypod.sidecar.container import (
    SIDECAR_CONTAINER,
    get_sidecar_args,
    get_sidecar_container,
)
from polyaxon.polypod.sidecar.env_vars import get_sidecar_env_vars
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestSidecarContainer(BaseTestCase):
    def assert_artifacts_store_raises(self, store, run_path=None):
        with self.assertRaises(PolypodException):
            get_sidecar_container(
                container_id=MAIN_JOB_CONTAINER,
                contexts=PluginsContextsSpec.from_config(
                    V1Plugins(collect_logs=True, collect_artifacts=False)
                ),
                env=None,
                polyaxon_sidecar=V1PolyaxonSidecarContainer(
                    image="sidecar/sidecar",
                    image_pull_policy="IfNotPresent",
                    sleep_interval=213,
                    sync_interval=213,
                ),
                artifacts_store=store,
                run_path=run_path,
            )

    def test_get_main_container_with_logs_store_with_wrong_paths_raises(self):
        artifacts_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        self.assert_artifacts_store_raises(store=artifacts_store)

        artifacts_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(volume_claim="foo", mount_path="/foo"),
        )
        self.assert_artifacts_store_raises(store=artifacts_store)

    def test_get_sidecar_container_without_an_artifacts_store(self):
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=None,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=213,
            ),
            artifacts_store=None,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path=None,
        )
        assert sidecar is None

    def test_get_sidecar_container_with_non_managed_mount_outputs_logs_store(self):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        mount_non_managed_store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                volume_claim="test", mount_path="/tmp", read_only=True
            ),
        )
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=-1,
            ),
            artifacts_store=mount_non_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, collect_artifacts=False, auth=True)
            ),
            run_path=None,
        )

        assert sidecar is None

    def test_get_sidecar_container_with_non_managed_bucket_artifacts_logs_store(self):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        bucket_non_managed_store = V1ConnectionType(
            name="test_s3",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=-1,
            ),
            artifacts_store=bucket_non_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, collect_artifacts=False, auth=True)
            ),
            run_path=None,
        )

        assert sidecar is None

    def test_get_sidecar_container_auth_context(
        self,
    ):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        resource1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="ref1", items=["item1", "item2"]),
            is_requested=False,
        )
        bucket_managed_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=resource1.schema,
        )

        # Default auth is included
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

        # Nno auth
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=-212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=False)),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.volume_mounts == [get_artifacts_context_mount(read_only=False)]

    def test_get_sidecar_container_with_managed_bucket_outputs_logs_store_and_env_secret(
        self,
    ):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        resource1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="ref1", items=["item1", "item2"]),
            is_requested=False,
        )
        bucket_managed_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=resource1.schema,
        )

        # Both logs/outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

        # logs and no outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=-212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=-212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
        ]

        # outputs and no logs
        sidecar = get_sidecar_container(
            container_id="test",
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id="test",
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id="test",
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

    def test_get_sidecar_container_with_managed_bucket_outputs_logs_store_and_mount_secret(
        self,
    ):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        resource1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(
                name="test1", items=["item1", "item2"], mount_path="/path"
            ),
            is_requested=False,
        )
        bucket_managed_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=resource1.schema,
        )

        # Both logs and outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_mount_from_resource(resource=resource1),
        ]

        # logs and no outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_mount_from_resource(resource=resource1),
        ]

        # outputs and no logs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_mount_from_resource(resource=resource1),
        ]

    def test_get_sidecar_container_with_managed_bucket_outputs_logs_store_and_env_from(
        self,
    ):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        resource1 = V1K8sResourceType(
            name="test1", schema=V1K8sResourceSchema(name="ref"), is_requested=False
        )
        bucket_managed_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=resource1.schema,
        )

        # both logs and outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == [get_env_from_secret(secret=resource1)]
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

        # logs and no outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == [get_env_from_secret(secret=resource1)]
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
        ]

        # outputs and no logs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=bucket_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=bucket_managed_store.name,
            )
            + get_items_from_secret(secret=resource1)
            + get_connection_env_var(connection=bucket_managed_store, secret=resource1)
        )
        assert sidecar.env_from == [get_env_from_secret(secret=resource1)]
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

    def test_get_sidecar_container_with_managed_mount_outputs_logs_store(self):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        mount_managed_store = V1ConnectionType(
            name="test_path",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(mount_path="/tmp", host_path="/tmp"),
            secret=None,
        )

        # logs and outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=mount_managed_store,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=mount_managed_store.name,
            )
            + get_connection_env_var(connection=mount_managed_store, secret=None)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_mount_from_store(store=mount_managed_store),
        ]

        # logs and no outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=mount_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=mount_managed_store.name,
            )
            + get_connection_env_var(connection=mount_managed_store, secret=None)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_mount_from_store(store=mount_managed_store),
        ]

        # outputs and no logs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=mount_managed_store,
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, auth=True)
            ),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=mount_managed_store.name,
            )
            + get_connection_env_var(connection=mount_managed_store, secret=None)
        )
        assert sidecar.env_from == []
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_mount_from_store(store=mount_managed_store),
        ]

    def test_get_sidecar_container_with_managed_mount_outputs_and_blob_logs_store(self):
        env_vars = [
            get_env_var(name="key1", value="value1"),
            get_env_var(name="key2", value="value2"),
        ]
        resource1 = V1K8sResourceType(
            name="test1", schema=V1K8sResourceSchema(name="ref1"), is_requested=False
        )
        blob_managed_store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.GCS,
            schema=V1BucketConnection(bucket="gs//:foo"),
            secret=resource1.schema,
        )

        # logs and outputs
        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            env=env_vars,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar",
                image_tag="",
                image_pull_policy="IfNotPresent",
                sleep_interval=213,
                sync_interval=212,
            ),
            artifacts_store=blob_managed_store,
            contexts=PluginsContextsSpec.from_config(None, default_auth=True),
            run_path="test",
        )

        assert sidecar.name == SIDECAR_CONTAINER
        assert sidecar.image == "sidecar/sidecar"
        assert sidecar.image_pull_policy == "IfNotPresent"
        assert sidecar.command == ["polyaxon", "sidecar"]
        assert sidecar.args == get_sidecar_args(
            container_id=MAIN_JOB_CONTAINER,
            sleep_interval=213,
            sync_interval=212,
            monitor_logs=False,
        )
        assert (
            sidecar.env
            == get_sidecar_env_vars(
                env_vars=env_vars,
                container_id=MAIN_JOB_CONTAINER,
                artifacts_store_name=blob_managed_store.name,
            )
            + get_connection_env_var(connection=blob_managed_store, secret=resource1)
        )
        assert sidecar.env_from == [get_env_from_secret(secret=resource1)]
        assert sidecar.resources == get_sidecar_resources()
        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
        ]

    def test_get_sidecar_container_host_paths(self):
        artifacts_store = V1ConnectionType(
            name="plx-outputs",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                mount_path="/tmp/plx/outputs", host_path="/tmp/plx/outputs"
            ),
        )

        contexts = PluginsContextsSpec(
            auth=True,
            docker=False,
            shm=False,
            collect_logs=True,
            collect_artifacts=True,
            collect_resources=True,
            auto_resume=True,
            sync_statuses=True,
            external_host=False,
        )

        sidecar = get_sidecar_container(
            container_id=MAIN_JOB_CONTAINER,
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="foo",
                image_pull_policy="sdf",
                sleep_interval=2,
                sync_interval=212,
            ),
            env=[],
            artifacts_store=artifacts_store,
            contexts=contexts,
            run_path="test",
        )

        assert sidecar.volume_mounts == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_mount_from_store(store=artifacts_store),
        ]
