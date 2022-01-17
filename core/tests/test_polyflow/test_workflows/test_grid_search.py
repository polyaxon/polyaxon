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

from marshmallow.exceptions import ValidationError

from polyaxon.polyflow import V1RunKind
from polyaxon.polyflow.matrix.grid_search import V1GridSearch
from polyaxon.polyflow.operations import V1CompiledOperation
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.workflow_mark
class TestWorkflowV1GridSearch(BaseTestCase):
    def test_grid_search_config(self):
        config_dict = {
            "kind": "grid",
            "numRuns": 10,
            "params": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["numRuns"] = -5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = -0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        # Add n_runs percent
        config_dict["numRuns"] = 0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = 5
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_grid_search_without_num_runs(self):
        config_dict = {
            "kind": "compiled_operation",
            "matrix": {
                "kind": "grid",
                "concurrency": 1,
                "params": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
                "earlyStopping": [],
            },
            "run": {"kind": V1RunKind.JOB, "container": {"image": "foo/bar"}},
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict


@pytest.mark.workflow_mark
class TestWorkflowV1GridSearchBackfill(BaseTestCase):
    def test_date_backfill_config(self):
        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "daterange",
                    "value": {
                        "start": "2019-06-22",
                        "stop": "2019-07-25",
                        "step": 4,
                    },
                }
            },
        }
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["numRuns"] = -5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = -0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        # Add n_runs percent
        config_dict["numRuns"] = 0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = 5
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_datetime_backfill_config(self):
        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "datetimerange",
                    "value": {
                        "start": "2019-06-22T12:12:00",
                        "stop": "2019-07-25T13:34:00",
                        "step": 4 * 3600,
                    },
                }
            },
        }
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["numRuns"] = -5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = -0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        # Add n_runs percent
        config_dict["numRuns"] = 0.5
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict["numRuns"] = 5
        config = V1GridSearch.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_wrong_date_backfill_config(self):
        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "daterange",
                    "value": ["2019-07-25", "2019-06-22", 2],
                }
            },
        }
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "daterange",
                    "value": ["2019-05-25", "2019-06-22 00:00", 2],
                }
            },
        }
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

    def test_wrong_datetime_backfill_config(self):
        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "datetimerange",
                    "value": ["2019-07-25 00:00", "2019-06-22 00:00", 3600 * 24],
                }
            },
        }
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)

        config_dict = {
            "kind": "grid",
            "concurrency": 1,
            "numRuns": 10,
            "params": {
                "dates": {
                    "kind": "datetimerange",
                    "value": ["2019-05-25", "2019-06-22 00:00", 3600 * 24],
                }
            },
        }
        with self.assertRaises(ValidationError):
            V1GridSearch.from_dict(config_dict)
