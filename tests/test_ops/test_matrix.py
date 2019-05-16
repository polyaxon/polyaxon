# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np

from unittest import TestCase

from marshmallow.exceptions import ValidationError

from polyaxon_schemas.ops.group.matrix import MatrixConfig


class TestMatrixConfigs(TestCase):
    def test_matrix_requires_at_least_one_value(self):
        config_dict = {}
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

    def test_matrix_accept_only_one_option(self):
        config_dict = {
            'values': [1, 2, 3],
            'linspace': '1:2:1'
        }
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

    def test_matrix_values_option(self):
        config_dict = {
            'values': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict['values']
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

        config_dict['values'] = ['ok', 'nook']
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict['values']
        assert config.sample() in ['ok', 'nook']
        assert config.length == 2
        assert config.is_categorical is True
        assert config.is_distribution is False
        assert config.is_range is False
        assert config.is_uniform is False
        assert config.is_discrete is True
        assert config.is_continuous is False
        assert config.min is None
        assert config.max is None

        config_dict['values'] = [[1, 2], [2, 4]]
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        assert config.to_numpy() == config_dict['values']
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
        config_dict = {
            'pvalues': [(1, 0.1), (2, 0.3), (3, 6)],
        }
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

        config_dict = {
            'pvalues': [(1, 0.1), (2, 0.3), (3, 0.8)],
        }
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

        config_dict = {
            'pvalues': [(1, 0.1), (2, 0.3), (3, -0.6)],
        }
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

        config_dict['pvalues'] = ['ok', 'nook']
        with self.assertRaises(ValidationError):
            MatrixConfig.from_dict(config_dict)

        # Pass for correct config
        config_dict = {
            'pvalues': [(1, 0.1), (2, 0.1), (3, 0.8)],
        }
        config = MatrixConfig.from_dict(config_dict)
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
            result = {'start': v1, 'stop': v2, 'step': v3}
            assert config.to_dict()['range'] == result
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
        config_dict = {
            'range': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['range'])

        # as string
        config_dict['range'] = '0:10:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict['range'] = {'start': 1.2, 'stop': 1.8, 'step': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_linspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {'start': v1, 'stop': v2, 'num': v3}
            assert config.to_dict()['linspace'] == result
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
        config_dict = {
            'linspace': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['linspace'])

        # as string
        config_dict['linspace'] = '0:10:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # as dict
        config_dict['linspace'] = {'start': 1.2, 'stop': 1.8, 'num': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_geomspace_option(self):
        def assert_equal(config, v1, v2, v3):
            result = {'start': v1, 'stop': v2, 'num': v3}
            assert config.to_dict()['geomspace'] == result
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
        config_dict = {
            'geomspace': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['geomspace'])

        # as string
        config_dict['geomspace'] = '1:10:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 1, 10, 1)

        # as dict
        config_dict['geomspace'] = {'start': 1.2, 'stop': 1.8, 'num': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_logspace_option(self):
        def assert_equal(config, v1, v2, v3, v4=None):
            result = {'start': v1, 'stop': v2, 'num': v3}
            if v4:
                result['base'] = v4

            assert config.to_dict()['logspace'] == result
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
        config_dict = {
            'logspace': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['logspace'])

        # with base
        config_dict['logspace'] = [1, 2, 3, 2]
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['logspace'])

        # as string
        config_dict['logspace'] = '0:10:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1)

        # with base
        config_dict['logspace'] = '0:10:1:2'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 10, 1, 2)

        # as dict
        config_dict['logspace'] = {'start': 1.2, 'stop': 1.8, 'num': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        # with base
        config_dict['logspace'] = {'start': 1.2, 'stop': 1.8, 'num': 0.1, 'base': 2}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_uniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {'low': v1, 'high': v2}
            if v3:
                result['size'] = v3
            assert config.to_dict()['uniform'] == result
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
        config_dict = {
            'uniform': [0, 1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['uniform'])

        # as string
        config_dict['uniform'] = '0:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict['uniform'] = {'low': 0, 'high': 1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_quniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {'low': v1, 'high': v2, 'q': q}
            if v3:
                result['size'] = v3
            assert config.to_dict()['quniform'] == result
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
        config_dict = {
            'quniform': [0, 1, 0.1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['quniform'])

        # as string
        config_dict['quniform'] = '0:1:0.1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict['quniform'] = {'low': 0, 'high': 1, 'q': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_loguniform_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {'low': v1, 'high': v2}
            if v3:
                result['size'] = v3
            assert config.to_dict()['loguniform'] == result
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
        config_dict = {
            'loguniform': [0, 1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['loguniform'])

        # as string
        config_dict['loguniform'] = '0:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict['loguniform'] = {'low': 0, 'high': 1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qloguniform_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {'low': v1, 'high': v2, 'q': q}
            if v3:
                result['size'] = v3
            assert config.to_dict()['qloguniform'] == result
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
        config_dict = {
            'qloguniform': [0, 1, 0.1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['qloguniform'])

        # as string
        config_dict['qloguniform'] = '0:1:0.1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict['qloguniform'] = {'low': 0, 'high': 1, 'q': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_normal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {'loc': v1, 'scale': v2}
            if v3:
                result['size'] = v3
            assert config.to_dict()['normal'] == result
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
        config_dict = {
            'normal': [0, 1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['normal'])

        # as string
        config_dict['normal'] = '0:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict['normal'] = {'loc': 0, 'scale': 1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qnormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {'loc': v1, 'scale': v2, 'q': q}
            if v3:
                result['size'] = v3
            assert config.to_dict()['qnormal'] == result
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
        config_dict = {
            'qnormal': [0, 1, 0.1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['qnormal'])

        # as string
        config_dict['qnormal'] = '0:1:0.1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict['qnormal'] = {'loc': 0, 'scale': 1, 'q': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_lognormal_option(self):
        def assert_equal(config, v1, v2, v3=None):
            result = {'loc': v1, 'scale': v2}
            if v3:
                result['size'] = v3
            assert config.to_dict()['lognormal'] == result
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
        config_dict = {
            'lognormal': [0, 1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['lognormal'])

        # as string
        config_dict['lognormal'] = '0:1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1)

        # as dict
        config_dict['lognormal'] = {'loc': 0, 'scale': 1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_qlognormal_option(self):
        def assert_equal(config, v1, v2, q, v3=None):
            result = {'loc': v1, 'scale': v2, 'q': q}
            if v3:
                result['size'] = v3
            assert config.to_dict()['qlognormal'] == result
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
        config_dict = {
            'qlognormal': [0, 1, 0.1],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, *config_dict['qlognormal'])

        # as string
        config_dict['qlognormal'] = '0:1:0.1'
        config = MatrixConfig.from_dict(config_dict)
        assert_equal(config, 0, 1, 0.1)

        # as dict
        config_dict['qlognormal'] = {'loc': 0, 'scale': 1, 'q': 0.1}
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
