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

from tests.utils import assert_equal_dict

from polyaxon.schemas.polyflow.early_stopping import (
    FailureEarlyStoppingConfig,
    MetricEarlyStoppingConfig,
)
from polyaxon.schemas.polyflow.optimization import Optimization


@pytest.mark.workflow_mark
class TestEarlyStoppingConfigs(TestCase):
    def test_metric_early_stopping(self):
        config_dict = {"kind": "metric_early_stopping", "metric": "loss", "value": 0.1}
        config = MetricEarlyStoppingConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict.pop("optimization") == Optimization.MAXIMIZE
        assert_equal_dict(config_to_dict, config_dict)

    def test_metric_early_stopping_with_median_policy(self):
        config_dict = {
            "kind": "metric_early_stopping",
            "metric": "loss",
            "value": 0.1,
            "optimization": Optimization.MINIMIZE,
            "policy": {"kind": "median", "evaluation_interval": 1},
        }
        config = MetricEarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_metric_early_stopping_with_average_policy(self):
        config_dict = {
            "kind": "metric_early_stopping",
            "metric": "loss",
            "value": 0.1,
            "optimization": Optimization.MINIMIZE,
            "policy": {"kind": "average", "evaluation_interval": 1},
        }
        config = MetricEarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_metric_early_stopping_with_truncation_policy(self):
        config_dict = {
            "kind": "metric_early_stopping",
            "metric": "loss",
            "value": 0.1,
            "optimization": Optimization.MAXIMIZE,
            "policy": {"kind": "truncation", "percent": 0.5, "evaluation_interval": 1},
        }
        config = MetricEarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_failure_early_stopping_with_truncation_policy(self):
        config_dict = {
            "kind": "failure_early_stopping",
            "percent": 0.3,
            "evaluation_interval": 1,
        }
        config = FailureEarlyStoppingConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
