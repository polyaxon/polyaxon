# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client import settings
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
                                    token='token',
                                    reraise=True,
                                    use_https=False)

    def test_base_urls(self):
        assert self.api_config.http_host == 'http://{}:{}'.format(self.host, self.http_port)
        assert self.api_config.ws_host == 'ws://{}:{}'.format(self.host, self.ws_port)
        assert self.api_config.base_url == 'http://{}:{}/api/v1'.format(self.host, self.http_port)
        assert self.api_config.base_ws_url == 'ws://{}:{}/ws/v1'.format(self.host, self.ws_port)

    def test_is_managed(self):
        settings.API_HTTP_HOST = 'api_host'
        settings.API_WS_HOST = 'ws_host'
        api_config = ApiConfig(host=None, http_port=None, ws_port=None, is_managed=True)
        assert api_config.version == 'v1'
        assert api_config.http_host == 'api_host'
        assert api_config.ws_host == 'ws_host'
        assert api_config.base_url == 'api_host/api/v1'
        assert api_config.base_ws_url == 'ws_host/ws/v1'
