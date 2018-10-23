# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from mock import patch

from polyaxon_cli.client import PolyaxonClient


class TestPolyaxonClient(TestCase):
    @patch('polyaxon_cli.client.client.GlobalConfigManager.get_value')
    @patch('polyaxon_cli.client.client.AuthConfigManager.get_value')
    def test_client(self, get_value_mock1, get_value_mock2):
        get_value_mock1.return_value = 'token'
        get_value_mock2.return_value = 'host'
        client = PolyaxonClient()

        assert client.host == 'host'
        assert client.token == 'token'
