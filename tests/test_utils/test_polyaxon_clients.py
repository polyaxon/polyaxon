# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from polyaxon_cli.client import PolyaxonClient


class TestPolyaxonClient(TestCase):
    @patch('polyaxon_cli.client.client.GlobalConfigManager.get_value')
    @patch('polyaxon_cli.client.client.AuthConfigManager.get_value')
    def test_client(self, get_value_mock1, get_value_mock2):
        get_value_mock1.return_value = None
        get_value_mock2.return_value = None

        client = PolyaxonClient()
        assert client.host is None
        assert client.http_port is None
        assert client.ws_port is None
        assert client.use_https is None
        assert client.token is None
