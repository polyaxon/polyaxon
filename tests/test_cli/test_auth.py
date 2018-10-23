# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.auth import logout, whoami


class TestAuth(BaseCommandTestCase):
    @patch('polyaxon_cli.managers.auth.AuthConfigManager.purge')
    def test_logout(self, get_user):
        self.runner.invoke(logout)
        assert get_user.call_count == 1

    @patch('polyaxon_client.api.auth.AuthApi.get_user')
    def test_whoami(self, get_user):
        self.runner.invoke(whoami)
        assert get_user.call_count == 1
