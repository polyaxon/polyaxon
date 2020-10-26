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

import numpy as np
import pytest

from mock import patch

from polyaxon.polytune.search_managers.bayesian_optimization.manager import (
    BayesSearchManager,
    V1Bayes,
)
from polyaxon.polytune.search_managers.bayesian_optimization.optimizer import (
    BOOptimizer,
)
from polyaxon.polytune.search_managers.bayesian_optimization.space import SearchSpace
from polyaxon.polytune.search_managers.random_search.manager import RandomSearchManager
from tests.utils import BaseTestCase


@pytest.mark.polytune_mark
class TestBayesSearchManager(BaseTestCase):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True
    DISABLE_AUDITOR = True

    def setUp(self):
        super().setUp()
        config = V1Bayes.from_dict(
            {
                "concurrency": 2,
                "maxIterations": 5,
                "numInitialRuns": 5,
                "metric": {"name": "loss", "optimization": "minimize"},
                "utilityFunction": {
                    "acquisitionFunction": "ucb",
                    "kappa": 1.2,
                    "gaussianProcess": {
                        "kernel": "matern",
                        "lengthScale": 1.0,
                        "nu": 1.9,
                        "numRestartsOptimizer": 0,
                    },
                },
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3]},
                    "feature2": {"kind": "linspace", "value": [1, 2, 5]},
                    "feature3": {"kind": "range", "value": [1, 5, 1]},
                },
            }
        )
        self.manager1 = BayesSearchManager(config=config)

        config = V1Bayes.from_dict(
            {
                "concurrency": 2,
                "maxIterations": 4,
                "numInitialRuns": 4,
                "metric": {"name": "accuracy", "optimization": "maximize"},
                "utilityFunction": {
                    "acquisitionFunction": "ei",
                    "eps": 1.2,
                    "gaussianProcess": {
                        "kernel": "matern",
                        "lengthScale": 1.0,
                        "nu": 1.9,
                        "numRestartsOptimizer": 0,
                    },
                },
                "params": {
                    "feature1": {"kind": "choice", "value": [1, 2, 3, 4, 5]},
                    "feature2": {"kind": "linspace", "value": [1, 5, 5]},
                    "feature3": {"kind": "range", "value": [1, 6, 1]},
                    "feature4": {"kind": "uniform", "value": [1, 5]},
                    "feature5": {"kind": "choice", "value": ["a", "b", "c"]},
                },
            }
        )
        self.manager2 = BayesSearchManager(config=config)

    def test_bo_search_config(self):
        assert BayesSearchManager.CONFIG == V1Bayes

    def test_first_get_suggestions_returns_initial_random_suggestion(self):
        assert len(self.manager1.get_suggestions()) == 5
        assert len(self.manager2.get_suggestions()) == 4

    def test_iteration_suggestions_calls_optimizer(self):
        with patch.object(
            RandomSearchManager, "get_suggestions"
        ) as get_suggestion_mock:
            self.manager1.get_suggestions()

        assert get_suggestion_mock.call_count == 1

        with patch.object(BOOptimizer, "get_suggestion") as get_suggestion_mock:
            self.manager1.get_suggestions(
                configs=[
                    {"feature1": 1, "feature2": 1, "feature3": 1},
                    {"feature1": 2, "feature2": 1.2, "feature3": 2},
                ],
                metrics=[1, 2],
            )

        assert get_suggestion_mock.call_count == 1

    def test_space_search(self):
        # Space 1
        space1 = SearchSpace(config=self.manager1.config)

        assert space1.dim == 3
        assert len(space1.bounds) == 3
        assert len(space1.discrete_features) == 3
        assert len(space1.categorical_features) == 0  # pylint:disable=len-as-condition

        for i, feature in enumerate(space1.features):
            # Bounds
            if feature == "feature1":
                assert np.all(space1.bounds[i] == [1, 3])
            elif feature == "feature2":
                assert np.all(space1.bounds[i] == [1, 2])
            elif feature == "feature3":
                assert np.all(space1.bounds[i] == [1, 5])

        for feature in space1.features:
            # Features
            if feature == "feature1":
                assert np.all(
                    space1.discrete_features["feature1"]["values"] == [1, 2, 3]
                )
            elif feature == "feature2":
                assert np.all(
                    space1.discrete_features["feature2"]["values"]
                    == np.asarray([1.0, 1.25, 1.5, 1.75, 2.0])
                )
            elif feature == "feature3":
                assert np.all(
                    space1.discrete_features["feature3"]["values"]
                    == np.asarray([1, 2, 3, 4])
                )

        # Space 2
        space2 = SearchSpace(config=self.manager2.config)

        assert space2.dim == 7
        assert len(space2.bounds) == 7
        assert len(space2.discrete_features) == 3
        assert len(space2.categorical_features) == 1
        assert len(space2.features) == 5

        for i, feature in enumerate(space2.features):
            # Bounds
            if feature == "feature1":
                assert np.all(space2.bounds[i] == [1, 5])
            elif feature == "feature2":
                assert np.all(space2.bounds[i] == [1, 5])
            elif feature == "feature3":
                assert np.all(space2.bounds[i] == [1, 6])
            elif feature == "feature4":
                assert np.all(space2.bounds[i] == [1, 5])
            elif feature == "feature5":
                assert np.all(space2.bounds[i] == [0, 1])

        # One feature left is continuous

        # One categorical Features
        assert space2.categorical_features == {
            "feature5": {"values": ["a", "b", "c"], "number": 3}
        }

        # 3 discrete Features
        assert space2.discrete_features["feature1"]["values"] == [1, 2, 3, 4, 5]
        assert np.all(
            space2.discrete_features["feature2"]["values"]
            == np.asarray([1, 2, 3, 4, 5])
        )
        assert np.all(
            space2.discrete_features["feature3"]["values"]
            == np.asarray([1, 2, 3, 4, 5])
        )

    def test_add_observation_to_space_search(self):
        space1 = SearchSpace(config=self.manager1.config)

        assert space1.x == []
        assert space1.y == []

        configs = [
            {"feature1": 1, "feature2": 1, "feature3": 1},
            {"feature1": 2, "feature2": 1.2, "feature3": 2},
            {"feature1": 3, "feature2": 1.3, "feature3": 3},
        ]
        metrics = [1, 2, 3]

        space1.add_observations(configs=configs, metrics=metrics)

        assert len(space1.x) == 3
        assert len(space1.y) == 3

        for i, feature in enumerate(space1.features):
            if feature == "feature1":
                assert np.all(space1.x[:, i] == [1, 2, 3])
            elif feature == "feature2":
                assert np.all(space1.x[:, i] == [1, 1.2, 1.3])
            elif feature == "feature3":
                assert np.all(space1.x[:, i] == [1, 2, 3])

        assert np.all(space1.y == np.array([-1, -2, -3]))

        space2 = SearchSpace(config=self.manager2.config)

        configs = [
            {
                "feature1": 1,
                "feature2": 1,
                "feature3": 1,
                "feature4": 1,
                "feature5": "a",
            },
            {
                "feature1": 2,
                "feature2": 1.2,
                "feature3": 2,
                "feature4": 4,
                "feature5": "b",
            },
            {
                "feature1": 3,
                "feature2": 1.3,
                "feature3": 3,
                "feature4": 3,
                "feature5": "a",
            },
        ]
        metrics = [1, 2, 3]

        space2.add_observations(configs=configs, metrics=metrics)

        assert len(space2.x) == 3
        assert len(space2.y) == 3

        for i, feature in enumerate(space2.features):
            if feature == "feature1":
                assert np.all(space2.x[:, i] == [1, 2, 3])
            elif feature == "feature2":
                assert np.all(space2.x[:, i] == [1, 1.2, 1.3])
            elif feature == "feature3":
                assert np.all(space2.x[:, i] == [1, 2, 3])
            elif feature == "feature4":
                assert np.all(space2.x[:, i] == [1, 4, 3])
            elif feature == "feature5":
                assert np.all(
                    space2.x[:, i : i + 3] == [[1, 0, 0], [0, 1, 0], [1, 0, 0]]
                )

        assert np.all(space2.y == np.array(metrics))

    def test_space_get_suggestion(self):
        space1 = SearchSpace(config=self.manager1.config)

        suggestion = space1.get_suggestion(suggestion=[1, 1, 1])
        assert suggestion == {"feature1": 1, "feature2": 1, "feature3": 1}

        suggestion = space1.get_suggestion(suggestion=[1, 1.2, 2])
        assert suggestion == {"feature1": 1, "feature2": 1.25, "feature3": 2}

        suggestion = space1.get_suggestion(suggestion=[1, 1.5, 3])
        assert suggestion == {"feature1": 1, "feature2": 1.5, "feature3": 3}

        space2 = SearchSpace(config=self.manager2.config)

        suggestion = space2.get_suggestion(suggestion=[1, 1, 1, 1, 1, 0, 0])
        assert suggestion == {
            "feature1": 1,
            "feature2": 1,
            "feature3": 1,
            "feature4": 1,
            "feature5": "a",
        }

        suggestion = space2.get_suggestion(suggestion=[1, 1.2, 2, 3, 0, 0, 1])
        assert suggestion == {
            "feature1": 1,
            "feature2": 1,
            "feature3": 2,
            "feature4": 3,
            "feature5": "c",
        }

        suggestion = space2.get_suggestion(suggestion=[1, 1.8, 3, 3, 0, 1, 0])
        assert suggestion == {
            "feature1": 1,
            "feature2": 2,
            "feature3": 3,
            "feature4": 3,
            "feature5": "b",
        }

    def test_optimizer_add_observations_calls_space_add_observations(self):
        optimizer = BOOptimizer(config=self.manager1.config)
        with patch.object(SearchSpace, "add_observations") as add_observations_mock:
            optimizer.add_observations(configs=[], metrics=[])

        assert add_observations_mock.call_count == 1

    def test_optimizer_get_suggestion(self):
        # Manager 1
        optimizer1 = BOOptimizer(config=self.manager1.config)
        optimizer1.N_ITER = 1
        optimizer1.N_WARMUP = 1

        configs = [
            {"feature1": 1, "feature2": 1, "feature3": 1},
            {"feature1": 1, "feature2": 1.2, "feature3": 1},
            {"feature1": 1, "feature2": 1, "feature3": 1},
            {"feature1": 1, "feature2": 1.11, "feature3": 1},
            {"feature1": 1, "feature2": 1.1, "feature3": 1},
            {"feature1": 1, "feature2": 1.21, "feature3": 1},
            {"feature1": 2, "feature2": 2, "feature3": 2},
            {"feature1": 3, "feature2": 2, "feature3": 2},
            {"feature1": 2, "feature2": 1.8, "feature3": 3},
            {"feature1": 3, "feature2": 2, "feature3": 3},
            {"feature1": 2, "feature2": 2, "feature3": 2},
            {"feature1": 3, "feature2": 2, "feature3": 2},
            {"feature1": 2, "feature2": 1.8, "feature3": 3},
            {"feature1": 3, "feature2": 2, "feature3": 3},
        ]
        metrics = [0, 1.1, 0.1, 0.1, 1.09, 0.4, 100, 200, 200, 300, 110, 210, 210, 310]

        optimizer1.add_observations(configs=configs, metrics=metrics)
        suggestion = optimizer1.get_suggestion()
        assert 1 <= suggestion["feature1"] <= 3
        assert 1 <= suggestion["feature2"] <= 2
        assert 1 <= suggestion["feature3"] <= 5

        # Manager 2
        optimizer2 = BOOptimizer(config=self.manager2.config)
        optimizer2.N_ITER = 1
        optimizer2.N_WARMUP = 1

        configs = [
            {
                "feature1": 1,
                "feature2": 1,
                "feature3": 1,
                "feature4": 1,
                "feature5": "a",
            },
            {
                "feature1": 2,
                "feature2": 1.2,
                "feature3": 2,
                "feature4": 4,
                "feature5": "b",
            },
            {
                "feature1": 3,
                "feature2": 1.3,
                "feature3": 3,
                "feature4": 3,
                "feature5": "a",
            },
        ]
        metrics = [1, 2, 3]

        optimizer2.add_observations(configs=configs, metrics=metrics)
        suggestion = optimizer2.get_suggestion()
        assert 1 <= suggestion["feature1"] <= 5
        assert 1 <= suggestion["feature2"] <= 5
        assert 1 <= suggestion["feature3"] <= 6
        assert 1 <= suggestion["feature4"] <= 5
        assert suggestion["feature5"] in ["a", "b", "c"]

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_concrete_example(self):
        config = V1Bayes.from_dict(
            {
                "concurrency": 2,
                "maxIterations": 5,
                "numInitialRuns": 10,
                "metric": {"name": "loss", "optimization": "minimize"},
                "utilityFunction": {
                    "acquisitionFunction": "ucb",
                    "kappa": 2.576,
                    "gaussianProcess": {
                        "kernel": "matern",
                        "lengthScale": 1.0,
                        "nu": 1.9,
                        "numRestartsOptimizer": 0,
                    },
                    "numWarmup": 1,
                    "numIterations": 1,
                },
                "params": {
                    "learning_rate": {"kind": "uniform", "value": [0.001, 0.01]},
                    "dropout": {"kind": "choice", "value": [0.25, 0.3]},
                    "activation": {"kind": "choice", "value": ["relu", "sigmoid"]},
                },
            }
        )
        optimizer = BOOptimizer(config=config)

        configs = [
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.004544653508229265,
                "activation": "sigmoid",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.005615296199690899,
                "activation": "sigmoid",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.008784330869587902,
                "activation": "sigmoid",
                "dropout": 0.25,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.0058591075447430065,
                "activation": "sigmoid",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.007464080062927171,
                "activation": "sigmoid",
                "dropout": 0.25,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.0024763129571936738,
                "activation": "relu",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.0074881581817925705,
                "activation": "sigmoid",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.003360405779075163,
                "activation": "relu",
                "dropout": 0.3,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.009916904455792564,
                "activation": "sigmoid",
                "dropout": 0.25,
            },
            {
                "num_epochs": 1,
                "num_steps": 300,
                "batch_size": 128,
                "learning_rate": 0.000881723263162717,
                "activation": "sigmoid",
                "dropout": 0.3,
            },
        ]
        metrics = [
            2.3018131256103516,
            2.302884340286255,
            2.3071441650390625,
            2.3034636974334717,
            2.301487922668457,
            0.05087224021553993,
            2.3032383918762207,
            0.06383182853460312,
            2.3120572566986084,
            0.7617478370666504,
        ]

        optimizer.add_observations(configs=configs, metrics=metrics)
        suggestion = optimizer.get_suggestion()

        assert 0.001 <= suggestion["learning_rate"] <= 0.01
        assert suggestion["dropout"] in [0.25, 0.3]
        assert suggestion["activation"] in ["relu", "sigmoid"]
