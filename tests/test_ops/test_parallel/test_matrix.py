# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np

from unittest import TestCase

import pytest

from marshmallow.exceptions import ValidationError

from polyaxon_schemas.ops.parallel.matrix import (
    MatrixChoiceConfig,
    MatrixGeomSpaceConfig,
    MatrixLinSpaceConfig,
    MatrixLogNormalConfig,
    MatrixLogSpaceConfig,
    MatrixLogUniformConfig,
    MatrixNormalConfig,
    MatrixPChoiceConfig,
    MatrixQLogNormalConfig,
    MatrixQLogUniformConfig,
    MatrixQNormalConfig,
    MatrixQUniformConfig,
    MatrixRangeConfig,
    MatrixUniformConfig,
)


@pytest.mark.parallel_mark
class TestMatrixConfigs(TestCase):
    def test_matrix_values_option(self):
        config_dict = {"kind": "choice", "value": [1, 2, 3]}
        config = MatrixChoiceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict["value"]
        assert config.sample() in [1, 2, 3]
        assert config.length == 3
        assert config.is_categorical is False
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert config.min == 1
        assert config.max == 3

        config_dict["value"] = ["ok", "nook"]
        config = MatrixChoiceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict["value"]
        assert config.sample() in ["ok", "nook"]
        assert config.length == 2
        assert config.is_categorical is True
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert config.min is None
        assert config.max is None

        config_dict["value"] = [[1, 2], [2, 4]]
        config = MatrixChoiceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict["value"]
        assert config.sample() in [[1, 2], [2, 4]]
        assert config.length == 2
        assert config.is_categorical is True
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert config.min is None
        assert config.max is None

    def test_matrix_pvalues_option(self):
        config_dict = {"kind": "pchoice", "value": [(1, 0.1), (2, 0.3), (3, 6)]}
        with self.assertRaises(ValidationError):
            MatrixPChoiceConfig.from_dict(config_dict)

        config_dict["value"] = [(1, 0.1), (2, 0.3), (3, 0.8)]
        with self.assertRaises(ValidationError):
            MatrixPChoiceConfig.from_dict(config_dict)

        config_dict["value"] = [(1, 0.1), (2, 0.3), (3, -0.6)]
        with self.assertRaises(ValidationError):
            MatrixPChoiceConfig.from_dict(config_dict)

        config_dict["value"] = ["ok", "nook"]
        with self.assertRaises(ValidationError):
            MatrixPChoiceConfig.from_dict(config_dict)

        # Pass for correct config
        config_dict["value"] = [(1, 0.1), (2, 0.1), (3, 0.8)]
        config = MatrixPChoiceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        with self.assertRaises(ValidationError):
            config.to_numpy()
        assert config.sample() in [1, 2, 3]
        assert config.length == 3
        assert config.is_categorical is False
        assert config.is_distribution is True
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert config.min is None
        assert config.max is None

    def test_matrix_range_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "step": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(config.to_numpy(), np.arange(**result))
            assert config.length == len(np.arange(**result))
            assert config.sample() in np.arange(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert config.min == v1
            assert config.max == v2

        # as list
        config_dict = {"kind": "range", "value": [1, 2, 3]}
        config = MatrixRangeConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = MatrixRangeConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "step": 0.1}
        config = MatrixRangeConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_linspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "num": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(config.to_numpy(), np.linspace(**result))
            assert config.length == len(np.linspace(**result))
            assert config.sample() in np.linspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert config.min == v1
            assert config.max == v2

        # as list
        config_dict = {"kind": "linspace", "value": [1, 2, 3]}
        config = MatrixLinSpaceConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = MatrixLinSpaceConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1}
        config = MatrixLinSpaceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_geomspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {"start": v1, "stop": v2, "num": v3}
            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(config.to_numpy(), np.geomspace(**result))
            assert config.length == len(np.geomspace(**result))
            assert config.sample() in np.geomspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert config.min == v1
            assert config.max == v2

        # as list
        config_dict = {"kind": "geomspace", "value": [1, 2, 3]}
        config = MatrixGeomSpaceConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "1:10:1"
        config = MatrixGeomSpaceConfig.from_dict(config_dict)
        assert_equal(config, 1, 10, 1)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1}
        config = MatrixGeomSpaceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_logspace_option(self):
        def assert_equal(config, v1, v2, v3, v4=None):
            result = {"start": v1, "stop": v2, "num": v3}
            if v4:
                result["base"] = v4

            assert config.to_dict()["value"] == result
            np.testing.assert_array_equal(config.to_numpy(), np.logspace(**result))
            assert config.length == len(np.logspace(**result))
            assert config.sample() in np.logspace(**result)
            assert config.is_categorical is False
            assert config.is_distribution is False
            assert config.is_range is True
            assert config.is_uniform is False
            assert config.is_discrete is True
            assert config.is_continuous is False
            assert config.min == v1
            assert config.max == v2

        # as list
        config_dict = {"kind": "logspace", "value": [1, 2, 3]}
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # with base
        config_dict["value"] = [1, 2, 3, 2]
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:10:1"
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # with base
        config_dict["value"] = "0:10:1:2"
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1, 2)

        # as dict
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1}
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # with base
        config_dict["value"] = {"start": 1.2, "stop": 1.8, "num": 0.1, "base": 2}
        config = MatrixLogSpaceConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_uniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"low": v1, "high": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert v1 <= config.sample() <= v2
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is True
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min == v1
            assert config.max == v2

        # as list
        config_dict = {"kind": "uniform", "value": [0, 1]}
        config = MatrixUniformConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = MatrixUniformConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1}
        config = MatrixUniformConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_quniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"low": v1, "high": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "quniform", "value": [0, 1, 0.1]}
        config = MatrixQUniformConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = MatrixQUniformConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1, "q": 0.1}
        config = MatrixQUniformConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_loguniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"low": v1, "high": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "loguniform", "value": [0, 1]}
        config = MatrixLogUniformConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = MatrixLogUniformConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1}
        config = MatrixLogUniformConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qloguniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"low": v1, "high": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "qloguniform", "value": [0, 1, 0.1]}
        config = MatrixQLogUniformConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = MatrixQLogUniformConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"low": 0, "high": 1, "q": 0.1}
        config = MatrixQLogUniformConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_normal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"loc": v1, "scale": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "normal", "value": [0, 1]}
        config = MatrixNormalConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = MatrixNormalConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1}
        config = MatrixNormalConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # as list
        config_dict["value"] = [66, 30]
        config = MatrixNormalConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "66:30"
        config = MatrixNormalConfig.from_dict(config_dict)
        assert_equal(config, 66, 30)

        # as dict
        config_dict["value"] = {"loc": 60, "scale": 30}
        config = MatrixNormalConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qnormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"loc": v1, "scale": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "qnormal", "value": [0, 1, 0.1]}
        config = MatrixQNormalConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = MatrixQNormalConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1, "q": 0.1}
        config = MatrixQNormalConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_lognormal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {"loc": v1, "scale": v2}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "lognormal", "value": [0, 1]}
        config = MatrixLogNormalConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1"
        config = MatrixLogNormalConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1}
        config = MatrixLogNormalConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qlognormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {"loc": v1, "scale": v2, "q": q}
            if v3:
                result["size"] = v3
            assert config.to_dict()["value"] == result
            with self.assertRaises(ValidationError):
                config.to_numpy()
            with self.assertRaises(ValidationError):
                config.length
            assert isinstance(config.sample(), float)
            assert config.is_categorical is False
            assert config.is_distribution is True
            assert config.is_range is False
            assert config.is_uniform is False
            assert config.is_discrete is False
            assert config.is_continuous is True
            assert config.min is None
            assert config.max is None

        # as list
        config_dict = {"kind": "qlognormal", "value": [0, 1, 0.1]}
        config = MatrixQLogNormalConfig.from_dict(config_dict)
        assert_equal(config, *config_dict["value"])

        # as string
        config_dict["value"] = "0:1:0.1"
        config = MatrixQLogNormalConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict["value"] = {"loc": 0, "scale": 1, "q": 0.1}
        config = MatrixQLogNormalConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
