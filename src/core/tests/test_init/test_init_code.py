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

import os
import pytest

from mock import patch

from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_GIT_CREDENTIALS,
    POLYAXON_KEYS_RUN_INSTANCE,
)
from polyaxon.exceptions import PolyaxonContainerException
from polyaxon.init.git import (
    create_code_repo,
    get_clone_url,
    has_cred_access,
    has_ssh_access,
)
from tests.utils import BaseTestCase


@pytest.mark.init_mark
class TestInitCode(BaseTestCase):
    def test_raise_if_env_var_not_found(self):
        with self.assertRaises(PolyaxonContainerException):
            create_code_repo(repo_path="", url="", revision="")

    def test_raise_if_env_var_not_correct(self):
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "foo"
        with self.assertRaises(PolyaxonContainerException):
            create_code_repo(repo_path="", url="", revision="")
        del os.environ[POLYAXON_KEYS_RUN_INSTANCE]

    def test_has_cred_access(self):
        assert has_cred_access() is False
        os.environ[POLYAXON_KEYS_GIT_CREDENTIALS] = "foo:bar"
        assert has_cred_access() is True
        del os.environ[POLYAXON_KEYS_GIT_CREDENTIALS]

    def test_has_ssh_access(self):
        assert has_ssh_access() is False

    def test_get_clone_url(self):
        url = "https://foo.com/test"
        assert get_clone_url(url=url) == url
        os.environ[POLYAXON_KEYS_GIT_CREDENTIALS] = "foo:bar"
        assert get_clone_url(url=url) == "https://foo:bar@foo.com/test"
        del os.environ[POLYAXON_KEYS_GIT_CREDENTIALS]

        with patch("polyaxon.init.git.has_ssh_access") as ssh_access_mock:
            ssh_access_mock.return_value = True
            assert get_clone_url(url=url) == "git@foo.com:test.git"

        url = "git@foo.com:test.git"
        with patch("polyaxon.init.git.has_ssh_access") as ssh_access_mock:
            ssh_access_mock.return_value = True
            assert get_clone_url(url=url) == "git@foo.com:test.git"
