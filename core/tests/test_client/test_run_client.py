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

import pytest
import uuid

from mock import MagicMock, mock

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.lifecycle import V1Statuses
from tests.utils import BaseTestCase


@pytest.mark.client_mark
class TestRunClient(BaseTestCase):
    @mock.patch("polyaxon_sdk.RunsV1Api.patch_run")
    def test_get_statuses(self, sdk_patch_run):
        client = RunClient(owner="owner", project="project", run_uuid=uuid.uuid4().hex)
        assert client.run_data.tags is None
        client.log_tags(["foo", "bar"])
        assert client.run_data.tags == ["foo", "bar"]
        assert sdk_patch_run.call_count == 1
