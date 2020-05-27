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

from unittest.mock import patch

import pytest

from tests.utils import BaseTestCase

from polyaxon.polyflow.matrix import V1GridSearch
from polyaxon.polytune.search_managers.grid_search.manager import GridSearchManager


@pytest.mark.polytune_mark
class TestGridSearch(BaseTestCase):
    def test_grid_search_config(self):
        assert GridSearchManager.CONFIG == V1GridSearch

    def test_get_suggestions(self):
        config = V1GridSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {"feature": {"kind": "choice", "value": [1, 2, 3]}},
            }
        )
        assert len(GridSearchManager(config).get_suggestions()) == 3

        config = V1GridSearch.from_dict(
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
        assert len(GridSearchManager(config).get_suggestions()) == 10

    def test_get_suggestions_calls_to_numpy(self):
        config = V1GridSearch.from_dict(
            {
                "concurrency": 2,
                "numRuns": 10,
                "params": {"feature": {"kind": "choice", "value": [1, 2, 3]}},
            }
        )
        with patch(
            "polyaxon.polytune.search_managers.grid_search.manager.to_numpy"
        ) as to_numpy_mock:
            GridSearchManager(config).get_suggestions()

        assert to_numpy_mock.call_count == 1

        config = V1GridSearch.from_dict(
            {
                "concurrency": 2,
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "logspace", "value": "0.01:0.1:5"},
                },
            }
        )
        with patch(
            "polyaxon.polytune.search_managers.grid_search.manager.to_numpy"
        ) as to_numpy_mock:
            GridSearchManager(config).get_suggestions()

        assert to_numpy_mock.call_count == 2
