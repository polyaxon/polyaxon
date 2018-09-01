# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client.api_config import ApiConfig
from polyaxon_client.transport import Transport


class TestBaseApi(TestCase):
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
        self.transport = Transport()


del TestBaseApi
