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

from mock import MagicMock, patch

from polyaxon.cli.artifacts import artifacts
from polyaxon_sdk import V1ProjectVersionKind
from tests.test_cli.utils import BaseCommandTestCase


@pytest.mark.cli_mark
class TestCliArtifacts(BaseCommandTestCase):
    @patch("polyaxon_sdk.ProjectsV1Api.create_version")
    @patch("polyaxon_sdk.ProjectsV1Api.patch_version")
    @patch("polyaxon_sdk.ProjectsV1Api.get_version")
    def test_create_artifact(self, get_version, patch_version, create_version):
        self.runner.invoke(artifacts, ["register"])
        assert create_version.call_count == 0
        assert patch_version.call_count == 0
        assert get_version.call_count == 0

        get_version.return_value = None
        self.runner.invoke(artifacts, ["register", "--project=owner/foo"])
        assert get_version.call_count == 1
        assert patch_version.call_count == 0
        assert create_version.call_count == 1

        get_version.return_value = MagicMock(
            kind=V1ProjectVersionKind.ARTIFACT,
        )
        self.runner.invoke(artifacts, ["register", "--project=owner/foo"])
        assert get_version.call_count == 2
        assert patch_version.call_count == 0
        assert create_version.call_count == 1
        self.runner.invoke(artifacts, ["register", "--project=owner/foo", "--force"])
        assert get_version.call_count == 3
        assert patch_version.call_count == 1
        assert create_version.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.list_versions")
    def test_list_artifacts(self, list_artifacts):
        self.runner.invoke(artifacts, ["ls", "--project=owner/foo"])
        assert list_artifacts.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.get_version")
    def test_get_artifact(self, get_artifact):
        self.runner.invoke(artifacts, ["get", "-p", "admin/foo"])
        assert get_artifact.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.patch_version")
    def test_update_artifact(self, update_artifact):
        self.runner.invoke(
            artifacts, ["update", "-p", "admin/foo", "--description=foo"]
        )
        assert update_artifact.call_count == 1

    @patch("polyaxon_sdk.ProjectsV1Api.create_version_stage")
    def test_update_artifact_stage(self, stage_artifact):
        self.runner.invoke(
            artifacts, ["stage", "-p", "admin/foo", "-to", "production", "--reason=foo"]
        )
        assert stage_artifact.call_count == 1
