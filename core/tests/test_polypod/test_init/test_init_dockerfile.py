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

from polyaxon.containers.containers import V1PolyaxonInitContainer, get_init_resources
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT,
)
from polyaxon.containers.names import INIT_DOCKERFILE_CONTAINER
from polyaxon.polyflow import V1Plugins
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.env_vars import get_run_instance_env_var
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.polypod.init.dockerfile import get_dockerfile_init_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types.dockerfile import V1DockerfileType


@pytest.mark.polypod_mark
class TestInitDockerfile(BaseTestCase):
    def test_get_dockerfile_init_container(self):
        dockerfile_args = V1DockerfileType(image="test/test")
        container = get_dockerfile_init_container(
            polyaxon_init=V1PolyaxonInitContainer(image="foo", image_tag=""),
            dockerfile_args=dockerfile_args,
            env=None,
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            run_path="test",
        )
        assert INIT_DOCKERFILE_CONTAINER.format("") in container.name
        assert container.image == "foo"
        assert container.image_pull_policy is None
        assert container.command == ["polyaxon", "docker", "generate"]
        assert container.args == [
            "--build-context={}".format(dockerfile_args.to_dict(dump=True)),
            "--destination={}".format(CONTEXT_MOUNT_ARTIFACTS),
            "--copy-path={}".format(CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("test")),
        ]
        assert container.env == [get_run_instance_env_var()]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=constants.CONTEXT_VOLUME_ARTIFACTS,
                mount_path=CONTEXT_MOUNT_ARTIFACTS,
            ),
            get_auth_context_mount(read_only=True),
        ]

        dockerfile_args = V1DockerfileType(
            image="test/test",
            lang_env="LANG",
            run=["step1", "step2"],
            env=[["key1", "val1"], ["key2", "val2"]],
            uid=2222,
            gid=2222,
        )
        container = get_dockerfile_init_container(
            polyaxon_init=V1PolyaxonInitContainer(
                image="init/init", image_tag="", image_pull_policy="IfNotPresent"
            ),
            env=[],
            dockerfile_args=dockerfile_args,
            mount_path="/somepath",
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            run_path="test",
        )
        assert INIT_DOCKERFILE_CONTAINER.format("") in container.name
        assert container.image == "init/init"
        assert container.image_pull_policy == "IfNotPresent"
        assert container.command == ["polyaxon", "docker", "generate"]
        assert container.args == [
            "--build-context={}".format(dockerfile_args.to_dict(dump=True)),
            "--destination=/somepath",
            "--copy-path={}".format(CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("test")),
        ]
        assert container.env == [get_run_instance_env_var()]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=get_volume_name("/somepath"), mount_path="/somepath"
            ),
            get_auth_context_mount(read_only=True),
        ]
