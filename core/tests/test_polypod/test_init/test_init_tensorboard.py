#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.auxiliaries import V1PolyaxonInitContainer, get_init_resources
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import V1BucketConnection, V1ClaimConnection
from polyaxon.containers.names import INIT_TENSORBOARD_CONTAINER_PREFIX
from polyaxon.contexts import paths as ctx_paths
from polyaxon.polyflow import V1Plugins
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
    get_mount_from_store,
)
from polyaxon.polypod.init.tensorboard import get_tensorboard_init_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1TensorboardType
from polyaxon.utils.test_utils import BaseTestCase


@pytest.mark.polypod_mark
class TestInitTensorboard(BaseTestCase):
    def test_get_tensorboard_init_container(self):
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.S3,
            tags=["test", "foo"],
            schema=V1BucketConnection(bucket="s3//:foo"),
        )
        tb_args = V1TensorboardType(
            port=6006,
            uuids="uuid1,  uuid2",
            use_names=True,
            path_prefix="/path/prefix",
            plugins="plug1, plug2",
        )
        container = get_tensorboard_init_container(
            polyaxon_init=V1PolyaxonInitContainer(image="foo", image_tag=""),
            tb_args=tb_args,
            artifacts_store=store,
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            run_instance="foo.bar.runs.uuid",
            env=None,
        )
        assert INIT_TENSORBOARD_CONTAINER_PREFIX in container.name
        assert container.image == "foo"
        assert container.image_pull_policy is None
        assert container.command == ["polyaxon", "initializer", "tensorboard"]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=constants.VOLUME_MOUNT_ARTIFACTS,
                mount_path=ctx_paths.CONTEXT_MOUNT_ARTIFACTS,
            ),
            get_auth_context_mount(read_only=True),
        ]
        assert container.args == [
            "--context-from=s3//:foo",
            "--context-to={}".format(ctx_paths.CONTEXT_MOUNT_ARTIFACTS),
            "--connection-kind=s3",
            "--port=6006",
            "--uuids=uuid1,uuid2",
            "--use-names",
            "--path-prefix=/path/prefix",
            "--plugins=plug1,plug2",
        ]

        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            tags=["test", "foo"],
            schema=V1ClaimConnection(
                mount_path="/claim/path", volume_claim="claim", read_only=True
            ),
        )
        tb_args = V1TensorboardType(
            port=2222, uuids="uuid1", use_names=False, plugins="plug1"
        )
        container = get_tensorboard_init_container(
            polyaxon_init=V1PolyaxonInitContainer(
                image="init/init", image_tag="", image_pull_policy="IfNotPresent"
            ),
            tb_args=tb_args,
            artifacts_store=store,
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=False)),
            run_instance="foo.bar.runs.uuid",
            env=None,
        )
        assert INIT_TENSORBOARD_CONTAINER_PREFIX in container.name
        assert container.image == "init/init"
        assert container.image_pull_policy == "IfNotPresent"
        assert container.command == ["polyaxon", "initializer", "tensorboard"]
        assert container.args == [
            "--context-from=/claim/path",
            "--context-to={}".format(ctx_paths.CONTEXT_MOUNT_ARTIFACTS),
            "--connection-kind=volume_claim",
            "--port=2222",
            "--uuids=uuid1",
            "--plugins=plug1",
        ]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=constants.VOLUME_MOUNT_ARTIFACTS,
                mount_path=ctx_paths.CONTEXT_MOUNT_ARTIFACTS,
            ),
            get_mount_from_store(store=store),
        ]
