# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch

from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.auth import logout, whoami


class TestAuth(BaseCommandTestCase):
    @patch('polyaxon_cli.managers.auth.AuthConfigManager.purge')
    def test_logout(self, purge_patch):
        self.runner.invoke(logout)
        assert purge_patch.call_count == 1

    @patch('polyaxon_client.auth.AuthClient.get_user')
    def test_whoami(self, purge_patch):
        self.runner.invoke(whoami)
        assert purge_patch.call_count == 1
