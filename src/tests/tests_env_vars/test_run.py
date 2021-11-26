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
from mock import patch

from polyaxon.env_vars.getters import get_project_run_or_local, get_run_or_local
from tests.utils import BaseTestCase


class TestRunEnvVars(BaseTestCase):
    def test_get_run_or_local(self):
        assert get_run_or_local("uuid") == "uuid"

    @patch("polyaxon.env_vars.getters.run.get_project_or_local")
    @patch("polyaxon.env_vars.getters.run.get_run_or_local")
    def test_get_project_run_or_local(
        self, get_run_or_local_mock, get_project_or_local_mock
    ):
        get_project_or_local_mock.return_value = ("owner", "project")
        get_run_or_local_mock.return_value = "uuid"

        assert get_project_run_or_local() == ("owner", "project", "uuid")
