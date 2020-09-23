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

from tests.utils import BaseTestCase

from polyaxon.managers.git import GitConfigManager
from polyaxon.polyflow import V1Init


@pytest.mark.managers_mark
class TestGitConfigManager(BaseTestCase):
    def test_default_props(self):
        assert GitConfigManager.is_global() is False
        assert GitConfigManager.is_local() is True
        assert GitConfigManager.IS_POLYAXON_DIR is False
        assert GitConfigManager.CONFIG_FILE_NAME == "polyaxongit.yaml"
        assert GitConfigManager.CONFIG == V1Init
