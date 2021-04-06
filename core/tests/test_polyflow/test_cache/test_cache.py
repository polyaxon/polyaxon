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

from polyaxon.polyflow import V1Cache
from tests.utils import BaseTestCase


@pytest.mark.components_mark
class TestCacheConfigs(BaseTestCase):
    def test_cache_config(self):
        config_dict = {"disable": True}
        assert config_dict == V1Cache.from_dict(config_dict).to_dict()

        config_dict = {"disable": True, "ttl": 12, "io": ["in1", "in2"]}
        assert config_dict == V1Cache.from_dict(config_dict).to_dict()
