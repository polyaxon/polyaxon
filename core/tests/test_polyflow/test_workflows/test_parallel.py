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
    GaussianProcessesKernels,
)
from polyaxon.polyflow.operations import V1CompiledOperation
from polyaxon.polyflow.optimization import V1Optimization, V1OptimizationMetric
from polyaxon.polyflow.run.kinds import V1RunKind


@pytest.mark.workflow_mark
class TestWorkflowConfigs(BaseTestCase):
    def test_workflow_config_raise_conditions(self):
        config_dict = {
            "kind": "compiled_operation",
            "matrix": {
                "kind": "mapping",
                "concurrency": 2,
                "values": [{"foo": 1}, {"foo": 2}, {"foo": 3}],
            },
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add random_search without matrix should raise
        config_dict["matrix"] = {"kind": "random", "numRuns": 10}
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        # Add a matrix definition with 2 methods
        config_dict["matrix"]["params"] = {
            "lr": {
                "kind": "choice",
                "value": [1, 2, 3],
                "pvalues": [(1, 0.3), (2, 0.3), (3, 0.3)],
            }
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        # Using a distribution with random search should pass
        config_dict["matrix"]["params"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add matrix definition should pass
        config_dict["matrix"]["params"] = {"lr": {"kind": "choice", "value": [1, 2, 3]}}
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add grid_search should raise
        config_dict["matrix"] = {"kind": "grid", "numRuns": 10}
        config_dict["matrix"]["params"] = {"lr": {"kind": "choice", "value": [1, 2, 3]}}
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Adding a distribution should raise
        config_dict["matrix"]["params"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        # Updating the matrix should pass
        config_dict["matrix"]["params"] = {"lr": {"kind": "choice", "value": [1, 2, 3]}}
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add hyperband should raise
        config_dict["matrix"] = {
            "kind": "hyperband",
            "maxIterations": 10,
            "eta": 3,
            "resource": {"name": "steps", "type": "int"},
            "resume": False,
            "metric": V1OptimizationMetric(
                name="loss", optimization=V1Optimization.MINIMIZE
            ).to_dict(),
            "params": {
                "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
            },
            "seed": 1,
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add early stopping
        config_dict["matrix"]["earlyStopping"] = [
            {
                "kind": "metric_early_stopping",
                "metric": "loss",
                "value": 0.1,
                "optimization": V1Optimization.MINIMIZE,
                "policy": {"kind": "median", "evaluationInterval": 1},
            },
            {
                "kind": "metric_early_stopping",
                "metric": "accuracy",
                "value": 0.9,
                "optimization": V1Optimization.MAXIMIZE,
                "policy": {
                    "kind": "truncation",
                    "percent": 50,
                    "evaluationInterval": 1,
                },
            },
        ]
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # Add bayes should raise
        config_dict["matrix"] = {
            "kind": "bayes",
            "metric": V1OptimizationMetric(
                name="loss", optimization=V1Optimization.MINIMIZE
            ).to_dict(),
            "numInitialRuns": 2,
            "numIterations": 10,
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
            "params": {
                "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
            },
            "seed": 1,
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        # Using non uniform distribution should raise
        # Updating the matrix should pass
        config_dict["matrix"]["params"] = {
            "lr": {"kind": "pchoice", "value": [[0.1, 0.1], [0.2, 0.9]]}
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        config_dict["matrix"]["params"] = {
            "lr": {"kind": "normal", "value": [0.1, 0.2]}
        }
        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        # Using uniform distribution should not raise
        config_dict["matrix"]["params"] = {
            "lr": {"kind": "uniform", "value": {"low": 0.1, "high": 0.2}}
        }
        config = V1CompiledOperation.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
