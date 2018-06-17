# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from faker import Faker
from unittest import TestCase

from polyaxon_client.base import PolyaxonClient

faker = Faker()


class TestBaseClient(TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.http_port = 8000
        self.ws_port = 1337
        self.client = PolyaxonClient(host=self.host,
                                     http_port=self.http_port,
                                     ws_port=self.ws_port,
                                     version='v1',
                                     token=None,
                                     reraise=True,
                                     use_https=False)

    def test_base_urls(self):
        assert self.client.http_host == 'http://{}:{}'.format(self.host, self.http_port)
        assert self.client.ws_host == 'ws://{}:{}'.format(self.host, self.ws_port)
        assert self.client.base_url == 'http://{}:{}/api/v1'.format(self.host, self.http_port)
        assert self.client.base_ws_url == 'ws://{}:{}/ws/v1'.format(self.host, self.ws_port)

    def test_get_page(self):
        assert self.client.get_page() == {}
        assert self.client.get_page(page=1) == {}
        assert self.client.get_page(page=2) == {'offset': self.client.PAGE_SIZE}
        assert self.client.get_page(page=3) == {'offset': self.client.PAGE_SIZE * 2}

    def test_build_url(self):
        assert self.client._build_url('a') == 'a/'
        assert self.client._build_url('a', 'b') == 'a/b/'

    def test_get_url(self):
        with self.assertRaises(self.client.errors_mapping['base']):
            self.client._get_url('a')

        assert self.client._get_url('base', 'endpoint') == 'base/endpoint/'
        assert self.client._get_http_url('endpoint') == '{}/endpoint/'.format(self.client.base_url)
        assert self.client._get_ws_url('endpoint') == '{}/endpoint/'.format(self.client.base_ws_url)

    def test_headers(self):
        assert self.client._get_headers() == {}
        assert self.client._get_headers({'key': 'value'}) == {'key': 'value'}
        self.client.token = 'token_hash'
        assert self.client._get_headers() == {"Authorization": "{} {}".format(
            self.client.authentication_type, self.client.token)}
