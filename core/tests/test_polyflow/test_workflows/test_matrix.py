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

from marshmallow.exceptions import ValidationError

from polyaxon.polyflow.matrix.params import (
    V1HpChoice,
    V1HpGeomSpace,
    V1HpLinSpace,
    V1HpLogNormal,
    V1HpLogSpace,
    V1HpLogUniform,
    V1HpNormal,
    V1HpPChoice,
    V1HpQLogNormal,
    V1HpQLogUniform,
    V1HpQNormal,
    V1HpQUniform,
    V1HpRange,
    V1HpUniform,
)
from polyaxon.polytune.matrix.utils import (
    get_length,
    get_max,
    get_min,
    sample,
    to_numpy,
)
from tests.utils import BaseTestCase


@pytest.mark.workflow_mark
class TestMatrixConfigs(BaseTestCase):
    def test_matrix_values_option(self):
        config_dict = {"kind": "choice", "value": [1, 2, 3]}
        config = V1HpChoice.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert to_numpy(config) == config_dict["value"]
        assert sample(config) in [1, 2, 3]
        assert get_length(config) == 3
        assert config.is_categorical is False
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert get_min(config) == 1
        assert get_max(config) == 3

        config_dict["value"] = ["ok", "nook"]
        config = V1HpChoice.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert to_numpy(config) == config_dict["value"]
        assert sample(config) in ["ok", "nook"]
        assert get_length(config) == 2
        assert config.is_categorical is True
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert get_min(config) is None
        assert get_max(config) is None

        config_dict["value"] = [[1, 2], [2, 4]]
        config = V1HpChoice.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert to_numpy(config) == config_dict["value"]
        assert sample(config) in [[1, 2], [2, 4]]
        assert get_length(config) == 2
        assert config.is_categorical is True
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert get_min(config) is None
        assert get_max(config) is None

    def test_matrix_pchoice_option(self):
        config_dict = {"kind": "pchoice", "value": [(1, 0.1), (2, 0.3), (3, 6)]}
        with self.assertRaises(ValidationError):
            V1HpPChoice.from_dict(config_dict)

        config_dict["value"] = [(1, 0.1), (2, 0.3), (3, 0.8)]
        with self.assertRaises(ValidationError):
            V1HpPChoice.from_dict(config_dict)

        config_dict["value"] = [(1, 0.1), (2, 0.3), (3, -0.6)]
        with self.assertRaises(ValidationError):
            V1HpPChoice.from_dict(config_dict)

        config_dict["value"] = ["ok", "nook"]
        with self.assertRaises(ValidationError):
            V1HpPChoice.from_dict(config_dict)

        # Pass for correct config
        config_dict["value"] = [(1, 0.1), (2, 0.1), (3, 0.8)]
        config = V1HpPChoice.from_dict(config_dict)
        assert config.to_dict() == config_dict
        with self.assertRaises(ValidationError):
            to_numpy(config)
        assert sample(config) in [1, 2, 3]
        assert get_length(config) == 3
        assert config.is_categorical is False
        assert config.is_distribution is True
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert get_min(config) is None
        assert get_max(config) is None

    def test_matrix_range_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "step": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(to_numpy(config), np.arange(**result))
            assert get_length(config) == len(np.arange(**result))
            assert sample(config) in np.arange(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert get_min(config) == v1
            assert get_max(config) == v2

        # as list
        config_dict = {"kind": "range", "value": [1, 2, 3]}
        config = V1HpRange.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = V1HpRange.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "step": 0.1}
        config = V1HpRange.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_linspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "num": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(to_numpy(config), np.linspace(**result))
            assert get_length(config) == len(np.linspace(**result))
            assert sample(config) in np.linspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert get_min(config) == v1
            assert get_max(config) == v2

        # as list
        config_dict = {"kind": "linspace", "value": [1, 2, 3]}
        config = V1HpLinSpace.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = V1HpLinSpace.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1}
        config = V1HpLinSpace.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_geomspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "num": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(to_numpy(config), np.geomspace(**result))
            assert get_length(config) == len(np.geomspace(**result))
            assert sample(config) in np.geomspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert get_min(config) == v1
            assert get_max(config) == v2

        # as list
        config_dict = {"kind": "geomspace", "value": [1, 2, 3]}
        config = V1HpGeomSpace.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "1:10:1"
        config = V1HpGeomSpace.from_dict(config_dict)
        assert_equal(config, 1, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 1}
        config = V1HpGeomSpace.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_logspace_option(self):
        def assert_equal(config, v1, v2, v3, v4=None):
            result = {"start": v1, "stop": v2, "num": v3}
            if v4:
                result["base"] = v4

            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(to_numpy(config), np.logspace(**result))
            assert get_length(config) == len(np.logspace(**result))
            assert sample(config) in np.logspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert get_min(config) == v1
            assert get_max(config) == v2

        # as list
        config_dict = {"kind": "logspace", "value": [1, 2, 3]}
        config = V1HpLogSpace.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # with base
        config_dict["value"] = [1, 2, 3, 2]
        config = V1HpLogSpace.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = V1HpLogSpace.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # with base
        config_dict["value"] = "0:10:1:2"
        config = V1HpLogSpace.from_dict(config_dict)
        assert_equal(config, 0, 10, 1, 2)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1}
        config = V1HpLogSpace.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # with base
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1, "base": 2}
        config = V1HpLogSpace.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_uniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"low": v1, "high": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert v1 <= sample(config) <= v2
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is True
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) == v1
            assert get_max(config) == v2

        # as list
        config_dict = {"kind": "uniform", "value": [0, 1]}
        config = V1HpUniform.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = V1HpUniform.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1}
        config = V1HpUniform.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_quniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"low": v1, "high": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "quniform", "value": [0, 1, 0.1]}
        config = V1HpQUniform.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = V1HpQUniform.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1, "q": 0.1}
        config = V1HpQUniform.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_loguniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"low": v1, "high": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "loguniform", "value": [0, 1]}
        config = V1HpLogUniform.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = V1HpLogUniform.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1}
        config = V1HpLogUniform.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qloguniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"low": v1, "high": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "qloguniform", "value": [0, 1, 0.1]}
        config = V1HpQLogUniform.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = V1HpQLogUniform.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1, "q": 0.1}
        config = V1HpQLogUniform.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_normal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"loc": v1, "scale": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "normal", "value": [0, 1]}
        config = V1HpNormal.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = V1HpNormal.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1}
        config = V1HpNormal.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # as list
        config_dict["value"] = [66, 30]
        config = V1HpNormal.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "66:30"
        config = V1HpNormal.from_dict(config_dict)
        assert_equal(config, 66, 30)

        # as dict
        config_dict["value"] = {"loc": 60, "scale": 30}
        config = V1HpNormal.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qnormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"loc": v1, "scale": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "qnormal", "value": [0, 1, 0.1]}
        config = V1HpQNormal.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = V1HpQNormal.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1, "q": 0.1}
        config = V1HpQNormal.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_lognormal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"loc": v1, "scale": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "lognormal", "value": [0, 1]}
        config = V1HpLogNormal.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = V1HpLogNormal.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1}
        config = V1HpLogNormal.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qlognormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"loc": v1, "scale": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                to_numpy(config)
            with self.assertRaises(ValidationError):
                get_length(config)
            assert isinstance(sample(config), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert get_min(config) is None
            assert get_max(config) is None

        # as list
        config_dict = {"kind": "qlognormal", "value": [0, 1, 0.1]}
        config = V1HpQLogNormal.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = V1HpQLogNormal.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1, "q": 0.1}
        config = V1HpQLogNormal.from_dict(config_dict)
        assert config.to_dict() == config_dict
