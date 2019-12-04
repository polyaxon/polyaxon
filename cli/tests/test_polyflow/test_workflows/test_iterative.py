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

from polyaxon.schemas.polyflow.base import BaseComponentConfig
from polyaxon.schemas.polyflow.parallel.iterative import IterativeConfig


@pytest.mark.workflow_mark
class TestWorkflowIterativeConfigs(TestCase):
    def test_iterative_config(self):
        config_dict = {"kind": "iterative", "n_iterations": 10}
        config = IterativeConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["n_iterations"] = -5
        with self.assertRaises(ValidationError):
            IterativeConfig.from_dict(config_dict)

        config_dict["n_iterations"] = -0.5
        with self.assertRaises(ValidationError):
            IterativeConfig.from_dict(config_dict)

        # Add n_runs percent
        config_dict["n_iterations"] = 0.5
        with self.assertRaises(ValidationError):
            IterativeConfig.from_dict(config_dict)

        config_dict["n_iterations"] = 5
        config = IterativeConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_iterative_without_n_iterations(self):
        config_dict = {
            "parallel": {
                "kind": "iterative",
                "matrix": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
                "seed": 1,
            }
        }

        with self.assertRaises(ValidationError):
            BaseComponentConfig.from_dict(config_dict)

        config_dict["parallel"]["n_iterations"] = 10
        config = BaseComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
