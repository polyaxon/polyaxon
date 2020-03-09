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
import tempfile
import uuid

import pytest

from mock import patch
from tests.utils import BaseTestCase

from polyaxon.client.impersonate import create_context_auth, impersonate
from polyaxon.schemas.api.authentication import AccessTokenConfig


@pytest.mark.client_mark
class TestImpersonate(BaseTestCase):
    def test_create_context_auth(self):
        token = uuid.uuid4().hex
        context_mount = tempfile.mkdtemp()
        context_mount_auth = "{}/.polyaxonauth".format(context_mount)

        # Login without updating the token and without persistence
        if os.path.exists(context_mount_auth):
            os.remove(context_mount_auth)

        assert os.path.exists(context_mount_auth) is False
        create_context_auth(AccessTokenConfig(token=token), context_mount_auth)
        assert os.path.exists(context_mount_auth) is True

    @patch("polyaxon_sdk.RunsV1Api.impersonate_token")
    @patch("polyaxon_sdk.UsersV1Api.get_user")
    @patch("polyaxon.client.impersonate.create_context_auth")
    def test_login_impersonate(self, create_context, get_user, impersonate_token):

        impersonate(owner="owner", project="project", run_uuid=uuid.uuid4().hex)
        assert impersonate_token.call_count == 1
        assert get_user.call_count == 1
        assert create_context.call_count == 1
