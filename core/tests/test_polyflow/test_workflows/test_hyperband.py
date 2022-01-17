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

from polyaxon.polyflow.matrix import V1Hyperband
from polyaxon.polyflow.optimization import V1Optimization, V1OptimizationMetric
from tests.utils import BaseTestCase, assert_equal_dict


@pytest.mark.workflow_mark
class TestWorkflowV1Hyperbands(BaseTestCase):
    def test_hyperband_config(self):
        config_dict = {
            "kind": "hyperband",
            "maxIterations": 10,
            "eta": 3,
            "resource": {"name": "steps", "type": "int"},
            "resume": False,
            "metric": V1OptimizationMetric(
                name="loss", optimization=V1Optimization.MINIMIZE
            ).to_dict(),
            "params": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = V1Hyperband.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["maxIterations"] = 0
        with self.assertRaises(ValidationError):
            V1Hyperband.from_dict(config_dict)

        config_dict["maxIterations"] = -0.5
        with self.assertRaises(ValidationError):
            V1Hyperband.from_dict(config_dict)

        config_dict["maxIterations"] = 3
        # Add numRuns percent
        config_dict["eta"] = -0.5
        with self.assertRaises(ValidationError):
            V1Hyperband.from_dict(config_dict)

        config_dict["eta"] = 2.9
        config = V1Hyperband.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
