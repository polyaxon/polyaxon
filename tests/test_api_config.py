# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client.api_config import ApiConfig


class TestApiConfig(TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.http_port = 8000
        self.ws_port = 1337
        self.api_config = ApiConfig(host=self.host,
                                    http_port=self.http_port,
                                    ws_port=self.ws_port,
                                    version='v1',
                                    token=None,
                                    reraise=True,
                                    use_https=False)

    def test_base_urls(self):
        assert self.api_config.http_host == 'http://{}:{}'.format(self.host, self.http_port)
        assert self.api_config.ws_host == 'ws://{}:{}'.format(self.host, self.ws_port)
        assert self.api_config.base_url == 'http://{}:{}/api/v1'.format(self.host, self.http_port)
        assert self.api_config.base_ws_url == 'ws://{}:{}/ws/v1'.format(self.host, self.ws_port)
