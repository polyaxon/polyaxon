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

import uuid

from unittest import TestCase

from mock import MagicMock, mock

from polyaxon import settings
from polyaxon.client.statuses import get_run_statuses


class TestStatuses(TestCase):
    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses(self, sdk_get_run_statuses):
        for _ in get_run_statuses(
            owner="owner", project="project", run_uuid=uuid.uuid4().hex
        ):
            pass
        assert sdk_get_run_statuses.call_count == 1

    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses_watch(self, sdk_get_run_statuses):
        settings.CLIENT_CONFIG.watch_interval = 1
        for _ in get_run_statuses(
            owner="owner", project="project", run_uuid=uuid.uuid4().hex, watch=True
        ):
            resp = MagicMock(status="failed", status_conditions=[])
            sdk_get_run_statuses.return_value = resp
        assert sdk_get_run_statuses.call_count == 2
