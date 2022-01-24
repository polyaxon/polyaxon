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

import numpy as np
import pytest

from unittest import TestCase

from traceml.processors.importance_processors import calculate_importance


@pytest.mark.processors_mark
class TestFeatureImportance(TestCase):
    def test_params_empty(self):
        assert calculate_importance(None, None) is None

    def test_params_single(self):
        res = calculate_importance([4], [{"param1": 3}])
        exp = {"param1": {"correlation": None, "importance": 0.0}}
        assert res == exp

    def test_params_perfect(self):
        res = calculate_importance(
            [3, 4, 5], [{"param1": 3}, {"param1": 4}, {"param1": 5}]
        )
        exp = {"param1": {"correlation": 1.0, "importance": 1.0}}
        assert res == exp

    def test_params_2_count_3(self):
        res = calculate_importance(
            [1, 2, 3],
            [
                {
                    "param1": 1,
                    "param2": 3,
                },
                {
                    "param1": 2,
                    "param2": 2,
                },
                {
                    "param1": 3,
                    "param2": 1,
                },
            ],
        )
        exp = {
            "param1": {"correlation": 1.0, "importance": 0.464},
            "param2": {"correlation": -1.0, "importance": 0.536},
        }
        assert res == exp

    def test_params_str_bad(self):
        assert calculate_importance(["foo", "bar"], []) is None

    def test_params_mixed(self):
        res = calculate_importance(
            [1, 2], [{"param1": "str1", "param2": 1}, {"param1": 2, "param2": 2}]
        )
        # what is this?
        exp = {
            "param1_2": {"correlation": 1.0, "importance": 0.348},
            "param1_str1": {"correlation": -1.0, "importance": 0.308},
            "param2": {"correlation": 1.0, "importance": 0.344},
        }
        assert res == exp

    def test_params_nan(self):
        assert (
            calculate_importance(
                [np.nan, 2], [{"param1": 3, "param2": 1}, {"param1": 2, "param2": 2}]
            )
            is None
        )

    def test_params_dict(self):
        assert calculate_importance([{"foo": 2, "bar": 4}], []) is None
