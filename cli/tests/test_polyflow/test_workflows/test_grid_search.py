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

import pytest

from marshmallow.exceptions import ValidationError
from tests.utils import assert_equal_dict

from polyaxon.schemas.polyflow.workflows import GridSearchConfig, WorkflowConfig


@pytest.mark.workflow_mark
class TestWorkflowGridSearchConfigs(TestCase):
    def test_grid_search_config(self):
        config_dict = {
            "kind": "grid_search",
            "n_experiments": 10,
            "matrix": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = GridSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["n_experiments"] = -5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        config_dict["n_experiments"] = -0.5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        # Add n_experiments percent
        config_dict["n_experiments"] = 0.5
        with self.assertRaises(ValidationError):
            GridSearchConfig.from_dict(config_dict)

        config_dict["n_experiments"] = 5
        config = GridSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_grid_search_without_n_experiments(self):
        config_dict = {
            "concurrency": 1,
            "strategy": {
                "kind": "grid_search",
                "matrix": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
            },
            "early_stopping": [],
        }
        config = WorkflowConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
