# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.user import user


class TestUser(BaseCommandTestCase):
    @patch('polyaxon_client.api.user.UserApi.activate_user')
    @patch('polyaxon_cli.cli.check.Printer.print_success')
    def test_activate(self, print_success, activate_user):
        self.runner.invoke(user, ['activate', 'username'])
        assert activate_user.call_count == 1
        assert print_success.call_count == 1

    @patch('polyaxon_client.api.user.UserApi.delete_user')
    @patch('polyaxon_cli.cli.check.Printer.print_success')
    def test_delete(self, print_success, delete_user):
        self.runner.invoke(user, ['delete', 'username'])
        assert delete_user.call_count == 1
        assert print_success.call_count == 1
