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

from polyaxon.env_vars.getters import get_project_error_message, get_project_or_local
from polyaxon.exceptions import PolyaxonClientException
from tests.utils import BaseTestCase


class TestProjectEnvVars(BaseTestCase):
    def test_get_project_error_message(self):
        assert get_project_error_message("", "") is not None
        assert get_project_error_message("test", "") is not None
        assert get_project_error_message("", "test") is not None
        assert get_project_error_message("test", "test") is None

    def test_get_project_or_local(self):
        with self.assertRaises(PolyaxonClientException):
            get_project_or_local(None)

        assert get_project_or_local("owner.project") == ("owner", "project")
