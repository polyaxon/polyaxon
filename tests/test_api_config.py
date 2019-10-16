# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon.client import settings
from polyaxon.client.config import ClientConfig


class TestClientConfig(TestCase):
    def setUp(self):
        self.host = "localhost"
        self.http_port = 8000
        self.ws_port = 1337
        self.config = ClientConfig(
            host=self.host,
            version="v1",
            token="token",
            reraise=True,
        )

    def test_base_urls(self):
        assert self.config.host == "http://{}:{}".format(
            self.host, self.http_port
        )
        assert self.config.base_url == "http://{}:{}/api/v1".format(
            self.host, self.http_port
        )

    def test_is_managed(self):
        settings.API_HOST = "api_host"
        config = ClientConfig(host=None, is_managed=True)
        assert config.version == "v1"
        assert config.host == "http://api_host:80"
        assert config.base_url == "http://api_host:80/api/v1"
