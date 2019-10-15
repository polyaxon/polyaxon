# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow.exceptions import ValidationError
from tests.utils import assert_equal_dict

from schemas.ops.parallel import (
    BOConfig,
    GridSearchConfig,
    HyperbandConfig,
    ParallelConfig,
    RandomSearchConfig,
)
from schemas.ops.parallel.bo import (
    AcquisitionFunctions,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
)
from schemas.ops.parallel.metrics import Optimization, SearchMetricConfig


@pytest.mark.parallel_mark
class TestParallelConfigs(TestCase):
    def test_grid_search_config(self):
        config_dict = {
            "kind": "grid",
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

    def test_random_search_config(self):
        config_dict = {
            "kind": "random",
            "n_experiments": 10,
            "matrix": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = RandomSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["n_experiments"] = -5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        config_dict["n_experiments"] = -0.5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        # Add n_experiments percent
        config_dict["n_experiments"] = 0.5
        with self.assertRaises(ValidationError):
            RandomSearchConfig.from_dict(config_dict)

        config_dict["n_experiments"] = 5
        config = RandomSearchConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_hyperband_config(self):
        config_dict = {
            "kind": "hyperband",
            "max_iter": 10,
            "eta": 3,
            "resource": {"name": "steps", "type": "int"},
            "resume": False,
            "metric": SearchMetricConfig(
                name="loss", optimization=Optimization.MINIMIZE
            ).to_dict(),
            "matrix": {"lr": {"kind": "choice", "value": [[0.1], [0.9]]}},
        }
        config = HyperbandConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["max_iter"] = 0
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict["max_iter"] = -0.5
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict["max_iter"] = 3
        # Add n_experiments percent
        config_dict["eta"] = -0.5
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict["eta"] = 2.9
        config = HyperbandConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

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
            "metric": SearchMetricConfig(
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

    def test_parallel_config_raise_conditions(self):
        config_dict = {"concurrency": 2}
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        config = ParallelConfig.from_dict(config.to_dict())
        assert_equal_dict(config.to_dict(), config_dict)

        # Add random_search without matrix should raise
        config_dict["algorithm"] = {"kind": "random", "n_experiments": 10}
        with self.assertRaises(TypeError):
            ParallelConfig.from_dict(config_dict)

        # Add a matrix definition with 2 methods
        config_dict["algorithm"]["matrix"] = {
            "lr": {
                "kind": "choice",
                "value": [1, 2, 3],
                "pvalues": [(1, 0.3), (2, 0.3), (3, 0.3)],
            }
        }
        with self.assertRaises(ValidationError):
            ParallelConfig.from_dict(config_dict)

        # Using a distribution with random search should pass
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_light_dict(), config_dict)

        # Add matrix definition should pass
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add grid_search should raise
        config_dict["algorithm"] = {"kind": "grid", "n_experiments": 10}
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Adding a distribution should raise
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
        }
        with self.assertRaises(ValidationError):
            ParallelConfig.from_dict(config_dict)

        # Updating the matrix should pass
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "choice", "value": [1, 2, 3]}
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add hyperband should raise
        config_dict["algorithm"] = {
            "kind": "hyperband",
            "max_iter": 10,
            "eta": 3,
            "resource": {"name": "steps", "type": "int"},
            "resume": False,
            "metric": SearchMetricConfig(
                name="loss", optimization=Optimization.MINIMIZE
            ).to_dict(),
            "matrix": {
                "lr": {"kind": "pchoice", "value": [(1, 0.3), (2, 0.3), (3, 0.3)]}
            },
            "seed": 1,
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add early stopping
        config_dict["early_stopping"] = [
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
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add bo should raise
        config_dict["algorithm"] = {
            "kind": "bo",
            "metric": SearchMetricConfig(
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
            ParallelConfig.from_dict(config_dict)

        # Using non uniform distribution should raise
        # Updating the matrix should pass
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "pchoice", "value": [[0.1, 0.1], [0.2, 0.9]]}
        }
        with self.assertRaises(ValidationError):
            ParallelConfig.from_dict(config_dict)

        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "normal", "value": [0.1, 0.2]}
        }
        with self.assertRaises(ValidationError):
            ParallelConfig.from_dict(config_dict)

        # Using uniform distribution should not raise
        config_dict["algorithm"]["matrix"] = {
            "lr": {"kind": "uniform", "value": {"low": 0.1, "high": 0.2}}
        }
        config = ParallelConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_random_and_grid_search_without_n_experiments(self):
        config_dict = {
            "concurrency": 1,
            "algorithm": {
                "kind": "random",
                "matrix": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
                "seed": 1,
            },
            "early_stopping": [],
        }
        config = ParallelConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "concurrency": 1,
            "algorithm": {
                "kind": "grid",
                "matrix": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
            },
            "early_stopping": [],
        }
        config = ParallelConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
