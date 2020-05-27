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

from marshmallow.exceptions import ValidationError
from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon.polyflow.matrix.bayes import (
    AcquisitionFunctions,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
    V1Bayes,
)
from polyaxon.polyflow.optimization import V1Optimization, V1OptimizationMetric


@pytest.mark.workflow_mark
class TestWorkflowV1Bayes(BaseTestCase):
    def test_gaussian_process_config(self):
        config_dict = {
            "kernel": GaussianProcessesKernels.MATERN,
            "lengthScale": 1.0,
            "nu": 1.9,
            "numRestartsOptimizer": 2,
        }
        config = GaussianProcessConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_utility_function_config(self):
        config_dict = {"acquisitionFunction": AcquisitionFunctions.UCB}
        with self.assertRaises(ValidationError):
            UtilityFunctionConfig.from_dict(config_dict)

        config_dict = {"acquisitionFunction": AcquisitionFunctions.POI}
        with self.assertRaises(ValidationError):
            UtilityFunctionConfig.from_dict(config_dict)

        config_dict = {
            "acquisitionFunction": AcquisitionFunctions.UCB,
            "kappa": 1.2,
            "gaussianProcess": {
                "kernel": GaussianProcessesKernels.MATERN,
                "lengthScale": 1.0,
                "nu": 1.9,
                "numRestartsOptimizer": 2,
            },
        }
        config = UtilityFunctionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "acquisitionFunction": AcquisitionFunctions.EI,
            "eps": 1.2,
            "gaussianProcess": {
                "kernel": GaussianProcessesKernels.MATERN,
                "lengthScale": 1.0,
                "nu": 1.9,
                "numRestartsOptimizer": 2,
            },
        }
        config = UtilityFunctionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_bayes_config(self):
        config_dict = {
            "kind": "bayes",
            "metric": V1OptimizationMetric(
                name="loss", optimization=V1Optimization.MINIMIZE
            ).to_dict(),
            "numInitialRuns": 2,
            "numIterations": 19,
            "utilityFunction": {
                "acquisitionFunction": AcquisitionFunctions.UCB,
                "kappa": 1.2,
                "gaussianProcess": {
                    "kernel": GaussianProcessesKernels.MATERN,
                    "lengthScale": 1.0,
                    "nu": 1.9,
                    "numRestartsOptimizer": 2,
                },
            },
            "params": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = V1Bayes.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
