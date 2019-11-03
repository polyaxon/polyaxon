#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.projects import projects


@pytest.mark.cli_mark
class TestCliProject(BaseCommandTestCase):
    @patch("polyaxon_sdk.ProjectsV1Api.create_project")
    def test_create_project(self, create_project):
        self.runner.invoke(projects, ["create"])
        assert create_project.call_count == 0
        self.runner.invoke(projects, ["create", "--name=foo"])
        assert create_project.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.list_projects")
    def test_list_projects(self, list_projects):
        self.runner.invoke(projects, ["ls"])
        assert list_projects.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.get_project")
    def test_get_project(self, get_project):
        self.runner.invoke(projects, ["-p admin/foo", "get"])
        assert get_project.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.patch_project")
    def test_update_project(self, update_project):
        self.runner.invoke(projects, ["update"])
        assert update_project.call_count == 0

        self.runner.invoke(projects, ["-p admin/foo", "update", "--description=foo"])
        assert update_project.call_count == 1

    # @patch("polyaxon_sdk.ProjectsV1Api.download_repo")  TODO
    # def test_project_download_repo(self, download_repo):
    #     self.runner.invoke(projects, ["-p admin/foo", "download"])
    #     assert download_repo.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.bookmark_project")
    def test_project_bookmark(self, bookmark):
        self.runner.invoke(projects, ["-p admin/foo", "bookmark"])
        assert bookmark.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.unbookmark_project")
    def test_project_unbookmark(self, unbookmark):
        self.runner.invoke(projects, ["-p admin/foo", "unbookmark"])
        assert unbookmark.call_count == 1
