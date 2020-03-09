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

import os
import uuid

import pytest

from mock import patch
from tests.utils import BaseTestCase

from polyaxon.env_vars.keys import POLYAXON_KEYS_RUN_INSTANCE
from polyaxon.exceptions import PolyaxonContainerException
from polyaxon.init.auth import create_auth_context


@pytest.mark.init_mark
class TestInitAuth(BaseTestCase):
    def test_raise_if_env_var_not_found(self):
        with self.assertRaises(PolyaxonContainerException):
            create_auth_context()

    def test_raise_if_env_var_not_correct(self):
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "foo"
        with self.assertRaises(PolyaxonContainerException):
            create_auth_context()
        del os.environ[POLYAXON_KEYS_RUN_INSTANCE]

    @patch("polyaxon_sdk.RunsV1Api.impersonate_token")
    @patch("polyaxon_sdk.UsersV1Api.get_user")
    @patch("polyaxon.client.impersonate.create_context_auth")
    def test_init_auth(self, create_context, get_user, impersonate_token):
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "owner.project.runs.{}".format(
            uuid.uuid4().hex
        )
        create_auth_context()
        assert impersonate_token.call_count == 1
        assert create_context.call_count == 1
        assert get_user.call_count == 1
        del os.environ[POLYAXON_KEYS_RUN_INSTANCE]
