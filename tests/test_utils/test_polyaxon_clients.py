# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from polyaxon_cli.utils.clients import PolyaxonClients


class TestPolyaxonClients(TestCase):
    @patch('polyaxon_cli.utils.clients.GlobalConfigManager.get_value')
    @patch('polyaxon_cli.utils.clients.AuthConfigManager.get_value')
    def test_clients(self, get_value_mock1, get_value_mock2):
        get_value_mock1.return_value = None
        get_value_mock2.return_value = None

        clients = PolyaxonClients()
        assert clients.host is None
        assert clients.http_port is None
        assert clients.ws_port is None
        assert clients.use_https is None
        assert clients.token is None
