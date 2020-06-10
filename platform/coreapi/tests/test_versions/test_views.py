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

from rest_framework import status

from polyaxon.api import API_V1
from polycommon import conf
from polycommon.options.registry.installation import PLATFORM_DIST, PLATFORM_VERSION
from tests.base.case import BaseTest


@pytest.mark.versions_mark
class TestInstallationVersionViewsV1(BaseTest):
    def setUp(self):
        super().setUp()
        self.installation_version = "/{}/version/".format(API_V1)

    def test_version(self):
        resp = self.client.get(self.installation_version)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["platform_version"] == conf.get(PLATFORM_VERSION)
        assert resp.data["platform_dist"] == conf.get(PLATFORM_DIST)
        assert set(resp.data.keys()) == {"platform_version", "platform_dist"}
