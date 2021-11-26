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

from polyaxon.polyflow import V1Join
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.hooks_mark
class TestJoinsConfigs(BaseTestCase):
    def test_join(self):
        config_dict = {
            "query": "metrics.a: < 21",
            "sort": "-inputs.name1",
            "params": {
                "a": {"value": "inputs.a"},
                "outputs": {"value": "outputs", "contextOnly": True},
            },
        }
        config = V1Join.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "query": "metrics.a: < 21",
            "sort": "-inputs.name1",
            "limit": 2,
            "params": {
                "output1": {"value": "outputs.output1", "connection": "test"},
            },
        }
        config = V1Join.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "query": "status: succeeded|failed",
            "params": {
                "events": {"value": "artifact.metric1.events", "toInit": True},
            },
        }
        config = V1Join.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
