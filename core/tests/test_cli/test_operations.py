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

from polyaxon.cli.operations import ops


@pytest.mark.cli_mark
class TestCliRuns(BaseCommandTestCase):
    @patch("polyaxon.client.RunClient.list")
    def test_list_runs(self, list_runs):
        self.runner.invoke(ops, ["-p admin/foo", "ls"])
        assert list_runs.call_count == 1

    @patch("polyaxon.client.RunClient.refresh_data")
    @patch("polyaxon.managers.project.ProjectManager.is_initialized")
    @patch("polyaxon.managers.project.ProjectManager.get_config")
    @patch("polyaxon.managers.run.RunManager.set_config")
    @patch("polyaxon.cli.operations.get_run_details")
    def test_get_run(
        self, get_run_details, set_config, is_initialized, get_config, get_run
    ):
        self.runner.invoke(
            ops,
            ["--project=admin/foo", "--uid=8aac02e3a62a4f0aaa257c59da5eab80", "get"],
        )
        assert get_run.call_count == 1
        assert set_config.call_count == 0
        assert is_initialized.call_count == 1
        assert get_config.call_count == 1
        assert get_run_details.call_count == 1

    @patch("polyaxon.client.RunClient.refresh_data")
    @patch("polyaxon.managers.project.ProjectManager.is_initialized")
    @patch("polyaxon.utils.cache._is_same_project")
    @patch("polyaxon.managers.run.RunManager.set_config")
    @patch("polyaxon.cli.operations.get_run_details")
    def test_get_run_cache(
        self, get_run_details, set_config, is_same_project, is_initialized, get_run
    ):
        is_initialized.return_value = True
        is_same_project.return_value = True
        self.runner.invoke(
            ops,
            ["--project=admin/foo", "--uid=8aac02e3a62a4f0aaa257c59da5eab80", "get"],
        )
        assert get_run.call_count == 1
        assert set_config.call_count == 1
        assert is_same_project.call_count == 1
        assert is_initialized.call_count == 1
        assert get_run_details.call_count == 1

    @patch("polyaxon.client.RunClient.update")
    def test_update_run(self, update_run):
        self.runner.invoke(ops, ["update"])
        assert update_run.call_count == 0

        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "update",
                "--description=foo",
            ],
        )
        assert update_run.call_count == 1

    @patch("polyaxon.client.RunClient.stop")
    def test_stop_run(self, stop):
        self.runner.invoke(ops, ["stop"])
        assert stop.call_count == 0

        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "stop",
                "-y",
            ],
        )
        assert stop.call_count == 1

    @patch("polyaxon.client.RunClient.restart")
    def test_restart_run(self, restart):
        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "restart",
            ],
        )
        assert restart.call_count == 1

    @patch("polyaxon.client.RunClient.restart")
    def test_copy_run(self, copy):
        self.runner.invoke(ops, ["restart"])
        assert copy.call_count == 0

        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "restart",
                "-c",
            ],
        )
        assert copy.call_count == 1

    @patch("polyaxon.client.RunClient.resume")
    def test_resume_run(self, resume):
        self.runner.invoke(
            ops,
            ["--project=admin/foo", "--uid=8aac02e3a62a4f0aaa257c59da5eab80", "resume"],
        )
        assert resume.call_count == 1

    @patch("polyaxon.client.RunClient.get_statuses")
    def test_run_statuses(self, get_statuses):
        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "statuses",
            ],
        )
        assert get_statuses.call_count == 1

    @patch("polyaxon.client.RunClient.download_artifacts")
    def test_run_download_artifacts(self, download_outputs):
        self.runner.invoke(
            ops,
            [
                "--project=admin/foo",
                "--uid=8aac02e3a62a4f0aaa257c59da5eab80",
                "artifacts",
            ],
        )
        assert download_outputs.call_count == 1
