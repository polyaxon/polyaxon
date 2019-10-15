# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.superuser import superuser


class TestSuperUser(BaseCommandTestCase):
    @patch('polyaxon.client.api.user.UserApi.grant_superuser')
    @patch('polyaxon.cli.check.Printer.print_success')
    def test_grant(self, print_success, grant_superuser):
        self.runner.invoke(superuser, ['grant', 'username'])
        assert grant_superuser.call_count == 1
        assert print_success.call_count == 1

    @patch('polyaxon.client.api.user.UserApi.revoke_superuser')
    @patch('polyaxon.cli.check.Printer.print_success')
    def test_revoke(self, print_success, revoke_superuser):
        self.runner.invoke(superuser, ['revoke', 'username'])
        assert revoke_superuser.call_count == 1
        assert print_success.call_count == 1
