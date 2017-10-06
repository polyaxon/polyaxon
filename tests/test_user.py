# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from polyaxon_schemas.user import UserConfig


class TestUserConfigs(TestCase):
    def test_project_config(self):
        config_dict = {'username': 'username',
                       'uuid': str(uuid.uuid4()),
                       'email': 'user@domain.com'}
        config = UserConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
