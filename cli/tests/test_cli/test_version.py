# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pytest

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.version import upgrade, version


@pytest.mark.cli_mark
class TestCliVersion(BaseCommandTestCase):
    @patch("polyaxon.cli.version.pip_upgrade")
    @patch("polyaxon.cli.version.sys")
    def test_upgrade(self, mock_sys, pip_upgrade):
        mock_sys.version = (
            "2.7.13 (default, Jan 19 2017, 14:48:08) \n[GCC 6.3.0 20170118]"
        )
        self.runner.invoke(upgrade)
        pip_upgrade.assert_called_once()

    @patch("polyaxon_sdk.VersionsV1Api.get_versions")
    @patch("polyaxon.cli.version.dict_tabulate")
    def test_versions(self, dict_tabulate, get_versions):
        self.runner.invoke(version)
        get_versions.assert_called_once()
        dict_tabulate.assert_called_once()
