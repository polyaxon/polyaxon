# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_deploy.schemas.rbac import RBACConfig


class TestRBACConfig(TestCase):
    def test_rbac_config(self):
        config_dict = {'enabled': True}
        config = RBACConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'enabled': False}
        config = RBACConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config = RBACConfig.from_dict({})
        assert config.to_dict() == {}
        assert config.to_light_dict() == {}
