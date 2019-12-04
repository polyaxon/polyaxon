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

from unittest import TestCase
from unittest.mock import patch

import pytest

from polyaxon.automl.search_managers.grid_search.manager import GridSearchManager
from polyaxon.schemas.polyflow.parallel import GridSearchConfig


@pytest.mark.automl_mark
class TestGridSearch(TestCase):
    def test_grid_search_config(self):
        assert GridSearchManager.CONFIG == GridSearchConfig

    def test_get_suggestions(self):
        config = GridSearchConfig.from_dict(
            {
                "concurrency": 2,
                "n_runs": 10,
                "matrix": {"feature": {"kind": "choice", "value": [1, 2, 3]}},
            }
        )
        assert len(GridSearchManager(config).get_suggestions()) == 3

        config = GridSearchConfig.from_dict(
            {
                "concurrency": 2,
                "n_runs": 10,
                "matrix": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "linspace", "value": [1, 2, 5]},
                    "feature3": {"kind": "range", "value": [1, 5, 1]},
                },
            }
        )
        assert len(GridSearchManager(config).get_suggestions()) == 10

    def test_get_suggestions_calls_to_numpy(self):
        config = GridSearchConfig.from_dict(
            {
                "concurrency": 2,
                "n_runs": 10,
                "matrix": {"feature": {"kind": "choice", "value": [1, 2, 3]}},
            }
        )
        with patch(
            "polyaxon.automl.search_managers.grid_search.manager.to_numpy"
        ) as to_numpy_mock:
            GridSearchManager(config).get_suggestions()

        assert to_numpy_mock.call_count == 1

        config = GridSearchConfig.from_dict(
            {
                "concurrency": 2,
                "matrix": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "logspace", "value": "0.01:0.1:5"},
                },
            }
        )
        with patch(
            "polyaxon.automl.search_managers.grid_search.manager.to_numpy"
        ) as to_numpy_mock:
            GridSearchManager(config).get_suggestions()

        assert to_numpy_mock.call_count == 2
