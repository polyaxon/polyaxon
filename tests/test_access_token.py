# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.access_token import AccessTokenConfig


class TestProjectConfigs(TestCase):
    def test_project_config(self):
        config_dict = {'username': 'username',
                       'token': 'sdfsdf098sdf80s9dSDF800'}
        config = AccessTokenConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
