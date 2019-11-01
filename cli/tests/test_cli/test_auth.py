# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.auth import logout, whoami


@pytest.mark.cli_mark
class TestCliAuth(BaseCommandTestCase):
    @patch("polyaxon.managers.auth.AuthConfigManager.purge")
    def test_logout(self, get_user):
        self.runner.invoke(logout)
        assert get_user.call_count == 1

    @patch("polyaxon_sdk.UsersV1Api.get_user")
    def test_whoami(self, get_user):
        self.runner.invoke(whoami)
        assert get_user.call_count == 1
