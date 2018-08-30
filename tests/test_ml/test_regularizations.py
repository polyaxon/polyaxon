# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ml.regularizations import (
    L1L2RegularizerConfig,
    L1RegularizerConfig,
    L2RegularizerConfig
)


class TestRegularizationConfigs(TestCase):
    def test_l1_config(self):
        config_dict = {
            'l': 0.5,
            'name': 'l1',
            'collect': False
        }
        config = L1RegularizerConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_l2_config(self):
        config_dict = {
            'l': 0.5,
            'name': 'l2',
            'collect': False
        }
        config = L2RegularizerConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_l2l1_config(self):
        config_dict = {
            'l1': 0.5,
            'l2': 0.5,
            'name': 'l2l1',
            'collect': True
        }
        config = L1L2RegularizerConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
