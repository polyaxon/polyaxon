# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon.client import settings
from polyaxon.client.api_config import ApiConfig


class TestApiConfig(TestCase):
    def setUp(self):
        self.host = "localhost"
        self.http_port = 8000
        self.ws_port = 1337
        self.api_config = ApiConfig(
            host=self.host,
            http_port=self.http_port,
            ws_port=self.ws_port,
            version="v1",
            token="token",
            reraise=True,
            use_https=False,
        )

    def test_base_urls(self):
        assert self.api_config.http_host == "http://{}:{}".format(
            self.host, self.http_port
        )
        assert self.api_config.ws_host == "ws://{}:{}".format(self.host, self.ws_port)
        assert self.api_config.base_url == "http://{}:{}/api/v1".format(
            self.host, self.http_port
        )
        assert self.api_config.base_ws_url == "ws://{}:{}/api/v1".format(
            self.host, self.ws_port
        )

    def test_is_managed(self):
        settings.API_HOST = "api_host"
        api_config = ApiConfig(host=None, http_port=None, ws_port=None, is_managed=True)
        assert api_config.version == "v1"
        assert api_config.http_host == "http://api_host:80"
        assert api_config.ws_host == "ws://api_host:80"
        assert api_config.base_url == "http://api_host:80/api/v1"
        assert api_config.base_ws_url == "ws://api_host:80/api/v1"
