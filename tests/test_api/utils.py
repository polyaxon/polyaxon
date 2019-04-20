# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile
import time

from unittest import TestCase

from mock import patch

from polyaxon_client import settings
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
                                    token='token',
                                    reraise=True,
                                    use_https=False,
                                    is_managed=False,
                                    interval=0,
                                    timeout=0.01,
                                    schema_response=True)
        self.transport = Transport(config=self.api_config)
        settings.TMP_AUTH_TOKEN_PATH = '{}/{}'.format(tempfile.mkdtemp(), '.plx')
        settings.USER_CLIENT_CONFIG_PATH = '{}/{}'.format(tempfile.mkdtemp(), '.plx')

    def set_raw_response(self):
        self.api_config.schema_response = False

    def set_schema_response(self):
        self.api_config.schema_response = True

    def assert_async_call(self, api_handler_call, method):
        with patch.object(Transport, method) as mock_fct:
            api_handler_call()
        time.sleep(0.02)
        assert mock_fct.call_count == 1

    def assert_periodic_call(self, api_handler_call, method):
        with patch.object(Transport, method) as mock_fct:
            api_handler_call()
        time.sleep(0.01)
        assert mock_fct.call_count == 1
