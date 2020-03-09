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

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.projects import project


@pytest.mark.cli_mark
class TestCliProject(BaseCommandTestCase):
    @patch("polyaxon.client.ProjectClient.create")
    def test_create_project(self, create_project):
        self.runner.invoke(project, ["create"])
        assert create_project.call_count == 0
        self.runner.invoke(project, ["create", "--owner=owner", "--name=foo"])
        assert create_project.call_count == 1

    @patch("polyaxon.client.ProjectClient.list")
    def test_list_projects(self, list_projects):
        self.runner.invoke(project, ["ls", "--owner=owner"])
        assert list_projects.call_count == 1

    @patch("polyaxon.client.ProjectClient.refresh_data")
    def test_get_project(self, get_project):
        self.runner.invoke(project, ["-p admin/foo", "get"])
        assert get_project.call_count == 1

    @patch("polyaxon.client.ProjectClient.update")
    def test_update_project(self, update_project):
        self.runner.invoke(project, ["update"])
        assert update_project.call_count == 0

        self.runner.invoke(project, ["-p admin/foo", "update", "--description=foo"])
        assert update_project.call_count == 1
