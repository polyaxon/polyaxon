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

import hyperopt

from polyaxon.polyflow.matrix.hyperopt import V1Hyperopt
from polyaxon.polytune.search_managers.hyperopt.manager import HyperoptManager
from tests.utils import BaseTestCase


@pytest.mark.polytune_mark
class TestHyperoptSearch(BaseTestCase):
    def test_hyperopt_search_config(self):
        assert HyperoptManager.CONFIG == V1Hyperopt

    def test_hyperopt_algorithm(self):
        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "rand",
                "numRuns": 1,
                "params": {"param": {"kind": "uniform", "value": [0.01, 0.5]}},
            }
        )
        manager = HyperoptManager(config)
        assert manager.algorithm == hyperopt.rand.suggest

        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "anneal",
                "numRuns": 1,
                "params": {"param": {"kind": "uniform", "value": [0.01, 0.5]}},
            }
        )
        manager = HyperoptManager(config)
        assert manager.algorithm == hyperopt.anneal.suggest

        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "tpe",
                "numRuns": 1,
                "params": {"param": {"kind": "uniform", "value": [0.01, 0.5]}},
            }
        )
        manager = HyperoptManager(config)
        assert manager.algorithm == hyperopt.tpe.suggest

    def test_search_space(self):
        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "rand",
                "numRuns": 1,
                "params": {
                    "param1": {"kind": "uniform", "value": [0.01, 0.5]},
                    "param2": {"kind": "quniform", "value": [0.01, 0.99, 0.1]},
                    "param3": {"kind": "normal", "value": [0, 0.99]},
                    "param4": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "param5": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                    "param6": {"kind": "linspace", "value": [0, 10, 1]},
                    "param7": {"kind": "geomspace", "value": [0.1, 1, 1]},
                },
            }
        )
        manager = HyperoptManager(config)
        assert set(manager._param_to_value.keys()) == {
            "param4",
            "param5",
            "param6",
            "param7",
        }
        assert set(manager._search_space.keys()) == {
            "param1",
            "param2",
            "param3",
            "param4",
            "param5",
            "param6",
            "param7",
        }

    def test_get_rand_suggestions(self):
        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "rand",
                "numRuns": 1,
                "params": {
                    "lr": {"kind": "uniform", "value": [0.01, 0.5]},
                    "dropout": {"kind": "uniform", "value": [0.01, 0.99]},
                    "batch": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "optimizer": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                },
            }
        )

        suggestion = HyperoptManager(config).get_suggestions()[0]

        self.assertTrue(0.99 >= suggestion["dropout"] >= 0.01)
        self.assertTrue(0.5 >= suggestion["lr"] >= 0.01)
        self.assertTrue(suggestion["batch"] in [32, 64, 126, 256])
        self.assertTrue(suggestion["optimizer"] in ["sgd", "adagrad", "adam", "ftrl"])

        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "rand",
                "numRuns": 10,
                "params": {
                    "lr": {"kind": "uniform", "value": [0.01, 0.5]},
                    "dropout": {"kind": "uniform", "value": [0.01, 0.99]},
                    "batch": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "optimizer": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                },
            }
        )

        assert len(HyperoptManager(config).get_suggestions()) == 10

    def test_get_anneal_suggestions(self):
        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "anneal",
                "numRuns": 1,  # TODO: no numRuns
                "params": {
                    "lr": {"kind": "uniform", "value": [0.01, 0.5]},
                    "dropout": {"kind": "uniform", "value": [0.01, 0.99]},
                    "batch": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "optimizer": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                },
            }
        )

        suggestion = HyperoptManager(config).get_suggestions()[0]

        self.assertTrue(0.99 >= suggestion["dropout"] >= 0.01)
        self.assertTrue(0.5 >= suggestion["lr"] >= 0.01)
        self.assertTrue(suggestion["batch"] in [32, 64, 126, 256])
        self.assertTrue(suggestion["optimizer"] in ["sgd", "adagrad", "adam", "ftrl"])

    def test_get_tpe_suggestions(self):
        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "tpe",
                "numRuns": 1,
                "params": {
                    "lr": {"kind": "uniform", "value": [0.01, 0.5]},
                    "dropout": {"kind": "uniform", "value": [0.01, 0.99]},
                    "batch": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "optimizer": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                },
            }
        )

        suggestion = HyperoptManager(config).get_suggestions()[0]

        self.assertTrue(0.99 >= suggestion["dropout"] >= 0.01)
        self.assertTrue(0.5 >= suggestion["lr"] >= 0.01)
        self.assertTrue(suggestion["batch"] in [32, 64, 126, 256])
        self.assertTrue(suggestion["optimizer"] in ["sgd", "adagrad", "adam", "ftrl"])

        config = V1Hyperopt.from_dict(
            {
                "concurrency": 2,
                "algorithm": "tpe",
                "numRuns": 10,
                "params": {
                    "lr": {"kind": "uniform", "value": [0.01, 0.5]},
                    "dropout": {"kind": "uniform", "value": [0.01, 0.99]},
                    "batch": {"kind": "choice", "value": [32, 64, 126, 256]},
                    "optimizer": {
                        "kind": "choice",
                        "value": ["sgd", "adagrad", "adam", "ftrl"],
                    },
                },
            }
        )

        assert len(HyperoptManager(config).get_suggestions()) == 10
