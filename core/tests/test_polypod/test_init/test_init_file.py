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

from polyaxon.auxiliaries import V1PolyaxonInitContainer, get_init_resources
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT,
)
from polyaxon.containers.names import INIT_FILE_CONTAINER_PREFIX
from polyaxon.polyflow import V1Plugins
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
)
from polyaxon.polypod.init.file import get_file_init_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1FileType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestInitFile(BaseTestCase):
    def test_get_file_init_container(self):
        file_args = V1FileType(content="test")
        container = get_file_init_container(
            polyaxon_init=V1PolyaxonInitContainer(image="foo", image_tag=""),
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            file_args=V1FileType(content="test"),
            run_path="test",
            run_instance="foo.bar.runs.uuid",
        )
        assert INIT_FILE_CONTAINER_PREFIX in container.name
        assert container.image == "foo"
        assert container.image_pull_policy is None
        assert container.command == ["polyaxon", "initializer", "file"]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=constants.CONTEXT_VOLUME_ARTIFACTS,
                mount_path=CONTEXT_MOUNT_ARTIFACTS,
            ),
            get_auth_context_mount(read_only=True),
        ]
        assert file_args.to_dict(dump=True) == '{"content":"test"}'
        assert container.args == [
            "--file-context={}".format('{"content":"test","filename":"file"}'),
            "--filepath={}".format(CONTEXT_MOUNT_ARTIFACTS),
            "--copy-path={}".format(CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("test")),
            "--track",
        ]

        file_args = V1FileType(filename="test", content="test")
        container = get_file_init_container(
            polyaxon_init=V1PolyaxonInitContainer(
                image="init/init", image_tag="", image_pull_policy="IfNotPresent"
            ),
            contexts=PluginsContextsSpec.from_config(V1Plugins(auth=True)),
            file_args=file_args,
            run_path="test",
            run_instance="foo.bar.runs.uuid",
        )
        assert INIT_FILE_CONTAINER_PREFIX in container.name
        assert container.image == "init/init"
        assert container.image_pull_policy == "IfNotPresent"
        assert container.command == ["polyaxon", "initializer", "file"]
        assert container.args == [
            "--file-context={}".format(file_args.to_dict(dump=True)),
            "--filepath={}".format(CONTEXT_MOUNT_ARTIFACTS),
            "--copy-path={}".format(CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("test")),
            "--track",
        ]
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [
            get_connections_context_mount(
                name=constants.CONTEXT_VOLUME_ARTIFACTS,
                mount_path=CONTEXT_MOUNT_ARTIFACTS,
            ),
            get_auth_context_mount(read_only=True),
        ]
