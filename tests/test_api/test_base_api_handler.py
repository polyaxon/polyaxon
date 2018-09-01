# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import ERRORS_MAPPING


class TestBaseApiHandler(TestBaseApi):
    def setUp(self):
        super(TestBaseApiHandler, self).setUp()
        self.api_handler = BaseApiHandler(transport=self.transport, config=self.api_config)

    def test_get_page(self):
        assert self.api_handler.get_page() == {}
        assert self.api_handler.get_page(page=1) == {}
        assert self.api_handler.get_page(page=2) == {'offset': self.api_config.PAGE_SIZE}
        assert self.api_handler.get_page(page=3) == {'offset': self.api_config.PAGE_SIZE * 2}

    def test_build_url(self):
        assert self.api_handler._build_url('a') == 'a/'
        assert self.api_handler._build_url('a', 'b') == 'a/b/'

    def test_get_url(self):
        with self.assertRaises(ERRORS_MAPPING['base']):
            self.api_handler._get_url('a')

        assert self.api_handler._get_url('base', 'endpoint') == 'base/endpoint/'
        assert self.api_handler._get_http_url('endpoint') == '{}/endpoint/'.format(
            self.api_config.base_url)
        assert self.api_handler._get_ws_url('endpoint') == '{}/endpoint/'.format(
            self.api_config.base_ws_url)
