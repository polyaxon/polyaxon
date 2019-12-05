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

from polyaxon.schemas.polyflow.component import ComponentConfig
from polyaxon.schemas.polyflow.optimization import (
    Optimization,
    OptimizationMetricConfig,
)
from polyaxon.schemas.polyflow.parallel.bo import (
    AcquisitionFunctions,
    GaussianProcessesKernels,
)


@pytest.mark.workflow_mark
class TestWorkflowConfigs(TestCase):
    def test_workflow_config_raise_conditions(self):
        config_dict = {
            "parallel": {
                "kind": "mapping",
                "concurrency": 2,
                "values": [{"foo": 1}, {"foo": 2}, {"foo": 3}],
            },
            "run": {"kind": "container", "image": "foo/bar"},
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add random_search without matrix should raise
        config_dict["parallel"] = {"kind": "random_search", "n_runs": 10}
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        # Add a matrix definition with 2 methods
        config_dict["parallel"]["matrix"] = {
            "lr": {
                "kind": "choice",
                "value": [1, 2, 3],
                "pvalues": [(1, 0.3), (2, 0.3), (3, 0.3)],
            }
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        # Using a distribution with random search should pass
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add matrix definition should pass
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add grid_search should raise
        config_dict["parallel"] = {"kind": "grid_search", "n_runs": 10}
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Adding a distribution should raise
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        # Updating the matrix should pass
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add hyperband should raise
        config_dict["parallel"] = {
            "kind": "hyperband",
            "max_iter": 10,
            "eta": 3,
            "resource": {"name": "steps", "type": "int"},
            "resume": False,
            "metric": OptimizationMetricConfig(
                name="loss", optimization=Optimization.MINIMIZE
            ).to_dict(),
            "matrix": {
                "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
            },
            "seed": 1,
        }
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add early stopping
        config_dict["parallel"]["early_stopping"] = [
            {
                "kind": "metric_early_stopping",
                "metric": "loss",
                "value": 0.1,
                "optimization": Optimization.MINIMIZE,
                "policy": {"kind": "median", "evaluation_interval": 1},
            },
            {
                "kind": "metric_early_stopping",
                "metric": "accuracy",
                "value": 0.9,
                "optimization": Optimization.MAXIMIZE,
                "policy": {
                    "kind": "truncation",
                    "percent": 50,
                    "evaluation_interval": 1,
                },
            },
        ]
        config = ComponentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add bo should raise
        config_dict["parallel"] = {
            "kind": "bo",
            "metric": OptimizationMetricConfig(
                name="loss", optimization=Optimization.MINIMIZE
            ).to_dict(),
            "n_initial_trials": 2,
            "n_iterations": 10,
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
            "matrix": {
                "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
            },
            "seed": 1,
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        # Using non uniform distribution should raise
        # Updating the matrix should pass
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [[0.1, 0.1], [0.2, 0.9]]}
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "normal", "value": [0.1, 0.2]}
        }
        with self.assertRaises(ValidationError):
            ComponentConfig.from_dict(config_dict)

        # Using uniform distribution should not raise
        config_dict["parallel"]["matrix"] = {
            "lr": {"kind": "uniform", "value": {"low": 0.1, "high": 0.2}}
        }
        config = ComponentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
