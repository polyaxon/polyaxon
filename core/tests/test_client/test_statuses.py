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
import uuid

from mock import MagicMock, mock

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.lifecycle import V1Statuses
from tests.utils import BaseTestCase


@pytest.mark.client_mark
class TestStatuses(BaseTestCase):
    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses(self, sdk_get_run_statuses):
        client = RunClient(owner="owner", project="project", run_uuid=uuid.uuid4().hex)
        for _ in client.get_statuses():
            pass
        assert sdk_get_run_statuses.call_count == 1

    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses_watch(self, sdk_get_run_statuses):
        settings.CLIENT_CONFIG.watch_interval = 1
        client = RunClient(owner="owner", project="project", run_uuid=uuid.uuid4().hex)
        for _ in client.watch_statuses():
            resp = MagicMock(status=V1Statuses.FAILED, status_conditions=[])
            sdk_get_run_statuses.return_value = resp
        assert sdk_get_run_statuses.call_count == 2
