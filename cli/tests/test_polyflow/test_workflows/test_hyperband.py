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

from polyaxon.schemas.polyflow.workflows.automl.hyperband import HyperbandConfig
from polyaxon.schemas.polyflow.workflows.metrics import Optimization, SearchMetricConfig


@pytest.mark.workflow_mark
class TestWorkflowHyperbandConfigs(TestCase):
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
        # Add n_runs percent
        config_dict["eta"] = -0.5
        with self.assertRaises(ValidationError):
            HyperbandConfig.from_dict(config_dict)

        config_dict["eta"] = 2.9
        config = HyperbandConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
