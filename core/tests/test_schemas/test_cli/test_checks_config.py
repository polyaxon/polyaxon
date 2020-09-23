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

from datetime import timedelta

import pytest

from tests.utils import BaseTestCase

from polyaxon.env_vars.keys import POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK
from polyaxon.schemas.cli.checks_config import ChecksConfig
from polyaxon.utils.tz_utils import now


@pytest.mark.schemas_mark
class TestChecksConfig(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.filename = "{}/{}".format(tempfile.mkdtemp(), "config")

    def test_get_interval(self):
        config = ChecksConfig()
        assert config.get_interval(1) == 1
        assert config.get_interval(-1) == -1
        assert config.get_interval(-2) == -2
        assert config.get_interval() == ChecksConfig.INTERVAL
        os.environ[POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK] = "-1"
        assert config.get_interval() == -1
        os.environ[POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK] = "-2"
        assert config.get_interval() == ChecksConfig.INTERVAL
        os.environ[POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK] = "1"
        assert config.get_interval() == ChecksConfig.INTERVAL
        os.environ[POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK] = str(
            ChecksConfig.INTERVAL + 1
        )
        assert config.get_interval() == ChecksConfig.INTERVAL + 1

    def test_should_check(self):
        config = ChecksConfig(last_check=now())
        assert config.should_check(-1) is False
        assert config.should_check(0) is True

        config.last_check = now() - timedelta(seconds=10000)
        assert config.should_check(-1) is False
        assert config.should_check() is True
        assert config.should_check(100) is True
        assert config.should_check(100000) is False
