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

from unittest.mock import patch

from polyaxon.polyflow.matrix import V1RandomSearch
from polyaxon.polytune.search_managers.random_search.manager import RandomSearchManager
from tests.utils import BaseTestCase


@pytest.mark.polytune_mark
class TestRandomSearch(BaseTestCase):
    def test_random_search_config(self):
        assert RandomSearchManager.CONFIG == V1RandomSearch

    def test_get_suggestions(self):
        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2]},
                    "feature3": {"kind": "range", "value": [1, 3, 1]},
                },
            }
        )

        assert len(RandomSearchManager(config).get_suggestions()) == 4

        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {
                    "feature1": {"kind": "pchoice", "value": [(1, 0.1), (2, 0.6)]},
                    "feature3": {"kind": "range", "value": [1, 3, 1]},
                },
            }
        )

        assert len(RandomSearchManager(config).get_suggestions()) == 4

        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "linspace", "value": [1, 2, 5]},
                    "feature3": {"kind": "range", "value": [1, 5, 1]},
                },
            }
        )
        assert len(RandomSearchManager(config).get_suggestions()) == 10

        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {
                    "feature1": {
                        "kind": "pchoice",
                        "value": [(1, 0.3), (2, 0.3), (3, 0.3)],
                    },
                    "feature2": {"kind": "uniform", "value": [0, 1]},
                    "feature3": {"kind": "qlognormal", "value": [0, 0.5, 0.51]},
                },
            }
        )
        assert len(RandomSearchManager(config).get_suggestions()) == 10

    def test_get_suggestions_calls_sample(self):
        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 1,
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "linspace", "value": [1, 2, 5]},
                    "feature3": {"kind": "range", "value": [1, 5, 1]},
                },
            }
        )
        with patch(
            "polyaxon.polytune.search_managers.random_search.manager.sample"
        ) as sample_mock:
            RandomSearchManager(config).get_suggestions()

        assert sample_mock.call_count == 3

        config = V1RandomSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 1,
                "params": {
                    "feature1": {
                        "kind": "pchoice",
                        "value": [(1, 0.3), (2, 0.3), (3, 0.3)],
                    },
                    "feature2": {"kind": "uniform", "value": [0, 1]},
                    "feature3": {"kind": "qlognormal", "value": [0, 0.5, 0.51]},
                    "feature4": {"kind": "range", "value": [1, 5, 1]},
                },
            }
        )
        with patch(
            "polyaxon.polytune.search_managers.random_search.manager.sample"
        ) as sample_mock:
            RandomSearchManager(config).get_suggestions()

        assert sample_mock.call_count == 4
