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

from polyaxon.cli.runs import runs


@pytest.mark.cli_mark
class TestCliRuns(BaseCommandTestCase):
    @patch("polyaxon_sdk.RunsV1Api.list_runs")
    def test_list_runs(self, list_runs):
        self.runner.invoke(runs, ["-p admin/foo", "ls"])
        assert list_runs.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.get_run")
    @patch("polyaxon.managers.project.ProjectManager.is_initialized")
    @patch("polyaxon.managers.run.RunManager.set_config")
    @patch("polyaxon.cli.runs.get_run_details")
    def test_get_run(self, get_run_details, set_config, is_initialized, get_run):
        self.runner.invoke(
            runs,
            ["--project=admin/foo", "--uid=8aac02e3a62a4f0aaa257c59da5eab80", "get"],
        )
        assert get_run.call_count == 1
        assert set_config.call_count == 1
        assert is_initialized.call_count == 1
        assert get_run_details.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.patch_run")
    def test_update_run(self, update_run):
        self.runner.invoke(runs, ["update"])
        assert update_run.call_count == 0

        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "update",
                "--description=foo",
            ],
        )
        assert update_run.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.stop_run")
    def test_stop_run(self, stop):
        self.runner.invoke(runs, ["stop"])
        assert stop.call_count == 0

        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "stop",
                "-y",
            ],
        )
        assert stop.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.restart_run")
    def test_restart_run(self, restart):
        self.runner.invoke(runs, ["restart"])
        assert restart.call_count == 0

        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "restart",
            ],
        )
        assert restart.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.copy_run")
    def test_copy_run(self, copy):
        self.runner.invoke(runs, ["restart"])
        assert copy.call_count == 0

        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "restart",
                "-c",
            ],
        )
        assert copy.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.resume_run")
    def test_resume_run(self, resume):
        self.runner.invoke(runs, ["resume"])
        assert resume.call_count == 0

        self.runner.invoke(
            runs,
            ["--project=admin/foo", "--uid=8aac02e3a62a4f0aaa257c59da5eab80", "resume"],
        )
        assert resume.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_run_statuses(self, get_statuses):
        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "statuses",
            ],
        )
        assert get_statuses.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.download_outputs")
    def test_run_download_repo(self, download_outputs):
        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "outputs",
            ],
        )
        assert download_outputs.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.bookmark_run")
    def test_run_bookmark(self, bookmark):
        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "bookmark",
            ],
        )
        assert bookmark.call_count == 1

    @patch("polyaxon_sdk.RunsV1Api.unbookmark_run")
    def test_run_unbookmark(self, unbookmark):
        self.runner.invoke(
            runs,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "unbookmark",
            ],
        )
        assert unbookmark.call_count == 1
