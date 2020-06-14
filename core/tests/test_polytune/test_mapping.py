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

from polyaxon.polyflow import V1Mapping
from polyaxon.polytune.search_managers.mapping.manager import MappingManager


@pytest.mark.polytune_mark
class TestMapping(BaseTestCase):
    def test_mapping_config(self):
        assert MappingManager.CONFIG == V1Mapping

    def test_get_suggestions(self):
        config = V1Mapping.from_dict(
            {"concurrency": 2, "values": [{"a": 1, "b": 2}, {"a": 1.3, "b": 3}]}
        )
        assert len(MappingManager(config).get_suggestions()) == 2

        config = V1Mapping.from_dict(
            {
                "concurrency": 2,
                "values": [
                    {"feature1": 1, "feature2": 1, "feature3": 1},
                    {"feature1": 2, "feature2": 2, "feature3": 2},
                    {"feature1": 3, "feature2": 3, "feature3": 3},
                ],
            }
        )
        assert len(MappingManager(config).get_suggestions()) == 3
