# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.user import UserConfig


class TestUserConfigs(TestCase):
    def test_user_config(self):
        config_dict = {'username': 'username',
                       'email': 'user@domain.com',
                       'is_superuser': False}
        config = UserConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
