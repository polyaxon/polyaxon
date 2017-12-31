# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import numpy as np

from polyaxon_schemas.matrix import MatrixConfig


class TestMatrixConfigs(TestCase):
    def test_matrix_requires_at_least_one_value(self):
        config_dict = {}
        with self.assertRaises(ValueError):
            MatrixConfig.from_dict(config_dict)

    def test_matrix_accept_only_one_option(self):
        config_dict = {
            'values': [1, 2, 3],
            'linspace': '1:2:1'
        }
        with self.assertRaises(ValueError):
            MatrixConfig.from_dict(config_dict)

    def test_matrix_values_option(self):
        config_dict = {
            'values': [1, 2, 3],
        }
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict['values'] = ['ok', 'nook']
        config = MatrixConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_matrix_range_option(self):

        def assert_equal(config, v1, v2, v3):
            result = {'start': v1, 'stop': v2, 'step': v3}
            assert config.to_dict()['range'] == result
            np.testing.assert_array_equal(config.to_numpy(), np.arange(**result))

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

