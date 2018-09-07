# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from polyaxon_cli.client import PolyaxonClient
from polyaxon_cli.client.exceptions import PolyaxonException


class TestPolyaxonClient(TestCase):
    @patch('polyaxon_cli.client.client.GlobalConfigManager.get_value')
    @patch('polyaxon_cli.client.client.AuthConfigManager.get_value')
    def test_client(self, get_value_mock1, get_value_mock2):
        with self.assertRaises(PolyaxonException):
            get_value_mock1.return_value = None
            get_value_mock2.return_value = None
            PolyaxonClient()

        get_value_mock1.return_value = 'token'
        get_value_mock2.return_value = 'host'
        client = PolyaxonClient()

        assert client.host == 'host'
        assert client.token == 'token'
