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
from tests.utils import BaseTestCase

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1ClaimConnection,
    V1HostPathConnection,
    V1K8sResourceSchema,
)
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_CONFIGS,
    CONTEXT_MOUNT_DOCKER,
    CONTEXT_MOUNT_SHM,
)
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.mounts import (
    get_artifacts_context_mount,
    get_auth_context_mount,
    get_connections_context_mount,
    get_docker_context_mount,
    get_mount_from_resource,
    get_mount_from_store,
    get_mounts,
    get_shm_context_mount,
)
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


@pytest.mark.polypod_mark
class TestMounts(BaseTestCase):
    def test_get_mount_from_store(self):
        # Non bucket stores
        assert get_mount_from_store(store=None) is None
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        assert get_mount_from_store(store=store) is None

        # Claim store
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/tmp", volume_claim="test", read_only=True
            ),
        )
        mount = get_mount_from_store(store=store)
        assert mount.name == store.name
        assert mount.mount_path == store.schema.mount_path
        assert mount.read_only == store.schema.read_only

        # Host path
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.HOST_PATH,
            schema=V1HostPathConnection(
                mount_path="/tmp", host_path="/tmp", read_only=True
            ),
        )
        mount = get_mount_from_store(store=store)
        assert mount.name == store.name
        assert mount.mount_path == store.schema.mount_path
        assert mount.read_only == store.schema.read_only

    def test_get_mount_from_resource(self):
        # Non mouth resource
        assert get_mount_from_resource(None) is None
        resource = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="ref", items=["item1", "item2"]),
            is_requested=False,
        )
        assert get_mount_from_resource(resource=resource) is None

        # Resource with mount
        resource = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(
                name="ref", items=["item1", "item2"], mount_path="/tmp"
            ),
            is_requested=False,
        )
        mount = get_mount_from_resource(resource=resource)
        assert mount.name == resource.name
        assert mount.mount_path == resource.schema.mount_path
        assert mount.read_only is True

    def test_get_docker_context_mount(self):
        mount = get_docker_context_mount()
        assert mount.name == constants.CONTEXT_VOLUME_DOCKER
        assert mount.mount_path == CONTEXT_MOUNT_DOCKER

    def test_get_auth_context_mount(self):
        mount = get_auth_context_mount()
        assert mount.name == constants.CONTEXT_VOLUME_CONFIGS
        assert mount.mount_path == CONTEXT_MOUNT_CONFIGS
        assert mount.read_only is None
        mount = get_auth_context_mount(read_only=True)
        assert mount.read_only is True

    def test_get_artifacts_context_mount(self):
        mount = get_artifacts_context_mount()
        assert mount.name == constants.CONTEXT_VOLUME_ARTIFACTS
        assert mount.mount_path == CONTEXT_MOUNT_ARTIFACTS
        assert mount.read_only is None
        mount = get_artifacts_context_mount(read_only=True)
        assert mount.read_only is True

    def test_get_connections_context_mount(self):
        mount = get_connections_context_mount(name="test", mount_path="/test")
        assert mount.name == "test"
        assert mount.mount_path == "/test"
        assert mount.read_only is None

    def test_get_shm_context_mount(self):
        mount = get_shm_context_mount()
        assert mount.name == constants.CONTEXT_VOLUME_SHM
        assert mount.mount_path == CONTEXT_MOUNT_SHM
        assert mount.read_only is None

    def test_get_mounts(self):
        assert (
            get_mounts(
                use_auth_context=False,
                use_artifacts_context=False,
                use_docker_context=False,
                use_shm_context=False,
            )
            == []
        )
        assert get_mounts(
            use_auth_context=True,
            use_artifacts_context=True,
            use_docker_context=True,
            use_shm_context=True,
        ) == [
            get_auth_context_mount(read_only=True),
            get_artifacts_context_mount(read_only=False),
            get_docker_context_mount(),
            get_shm_context_mount(),
        ]
