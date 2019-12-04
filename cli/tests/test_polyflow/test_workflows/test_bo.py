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

from polyaxon.schemas.polyflow.optimization import (
    Optimization,
    OptimizationMetricConfig,
)
from polyaxon.schemas.polyflow.parallel.bo import (
    AcquisitionFunctions,
    BOConfig,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
)


@pytest.mark.workflow_mark
class TestWorkflowBOConfigs(TestCase):
    def test_gaussian_process_config(self):
        config_dict = {
            "kernel": GaussianProcessesKernels.MATERN,
            "length_scale": 1.0,
            "nu": 1.9,
            "n_restarts_optimizer": 2,
        }
        config = GaussianProcessConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_utility_function_config(self):
        config_dict = {"acquisition_function": AcquisitionFunctions.UCB}
        with self.assertRaises(ValidationError):
            UtilityFunctionConfig.from_dict(config_dict)

        config_dict = {"acquisition_function": AcquisitionFunctions.POI}
        with self.assertRaises(ValidationError):
            UtilityFunctionConfig.from_dict(config_dict)

        config_dict = {
            "acquisition_function": AcquisitionFunctions.UCB,
            "kappa": 1.2,
            "gaussian_process": {
                "kernel": GaussianProcessesKernels.MATERN,
                "length_scale": 1.0,
                "nu": 1.9,
                "n_restarts_optimizer": 2,
            },
        }
        config = UtilityFunctionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config_dict = {
            "acquisition_function": AcquisitionFunctions.EI,
            "eps": 1.2,
            "gaussian_process": {
                "kernel": GaussianProcessesKernels.MATERN,
                "length_scale": 1.0,
                "nu": 1.9,
                "n_restarts_optimizer": 2,
            },
        }
        config = UtilityFunctionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_bo_config(self):
        config_dict = {
            "kind": "bo",
            "metric": OptimizationMetricConfig(
                name="loss", optimization=Optimization.MINIMIZE
            ).to_dict(),
            "n_initial_trials": 2,
            "n_iterations": 19,
            "utility_function": {
                "acquisition_function": AcquisitionFunctions.UCB,
                "kappa": 1.2,
                "gaussian_process": {
                    "kernel": GaussianProcessesKernels.MATERN,
                    "length_scale": 1.0,
                    "nu": 1.9,
                    "n_restarts_optimizer": 2,
                },
            },
            "matrix": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = BOConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
