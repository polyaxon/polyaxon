# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.constraints import MaxNormConfig, MinMaxNormConfig, UnitNormConfig


class TestConstraintConfigs(TestCase):
    def test_max_norm_constraint_config(self):
        config_dict = {
            'max_value': 2,
            'axis': 1,
        }
        config = MaxNormConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_unit_norm_constraint_config(self):
        config_dict = {
            'axis': 1,
        }
        config = UnitNormConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_min_max_norm_constraint_config(self):
        config_dict = {
            'min_value': 1,
            'max_value': 2,
            'rate': 1.,
            'axis': 1,
        }
        config = MinMaxNormConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
