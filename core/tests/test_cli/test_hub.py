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

from mock import patch

from polyaxon.cli.hub import hub
from tests.test_cli.utils import BaseCommandTestCase


@pytest.mark.cli_mark
class TestCliHub(BaseCommandTestCase):
    @patch("polyaxon_sdk.ComponentHubV1Api.create_component_hub")
    def test_create_hub(self, create_hub):
        self.runner.invoke(hub, ["create"])
        assert create_hub.call_count == 0
        self.runner.invoke(hub, ["create", "--name=owner/foo"])
        assert create_hub.call_count == 1

    @patch("polyaxon_sdk.ComponentHubV1Api.list_component_hubs")
    def test_list_hubs(self, list_hub):
        self.runner.invoke(hub, ["ls", "--owner=owner"])
        assert list_hub.call_count == 1

    @patch("polyaxon_sdk.ComponentHubV1Api.get_component_hub")
    def test_get_hub(self, get_hub):
        self.runner.invoke(hub, ["get", "-c=admin/foo"])
        assert get_hub.call_count == 1

    @patch("polyaxon_sdk.ComponentHubV1Api.patch_component_hub")
    def test_update_hub(self, update_hub):
        self.runner.invoke(hub, ["update", "-c=admin/foo", "--description=foo"])
        assert update_hub.call_count == 1
