# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_deploy.schemas.ssl import SSLConfig


class TestSSLConfig(TestCase):
    def test_ssl_config(self):
        config_dict = {'enabled': True, 'secretName': 'foo', 'path': '/etc/ssl'}
        config = SSLConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
