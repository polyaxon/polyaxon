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

from polyaxon.auxiliaries import V1PolyaxonInitContainer, get_init_resources
from polyaxon.containers.names import INIT_AUTH_CONTAINER
from polyaxon.polypod.common.mounts import get_auth_context_mount
from polyaxon.polypod.init.auth import get_auth_context_container
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestInitAuth(BaseTestCase):
    def test_get_auth_context_container(self):
        container = get_auth_context_container(
            polyaxon_init=V1PolyaxonInitContainer(
                image="foo/foo", image_tag="", image_pull_policy="IfNotPresent"
            ),
            env=[],
        )

        assert container.name == INIT_AUTH_CONTAINER
        assert container.image == "foo/foo"
        assert container.image_pull_policy == "IfNotPresent"
        assert container.command == ["polyaxon", "initializer", "auth"]
        assert container.args is None
        assert container.env == []
        assert container.resources == get_init_resources()
        assert container.volume_mounts == [get_auth_context_mount(read_only=False)]
