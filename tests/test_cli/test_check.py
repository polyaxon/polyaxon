# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import pytest
from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.check import check


@pytest.mark.cli_mark
class TestCliCheck(BaseCommandTestCase):
    @patch("polyaxon.cli.check.check_polyaxonfile")
    def test_check_file(self, check_polyaxonfile):
        self.runner.invoke(check)
        assert check_polyaxonfile.call_count == 1

    @patch("polyaxon.cli.check.check_polyaxonfile")
    @patch("polyaxon.cli.check.Printer.decorate_format_value")
    def test_check_file_version(self, decorate_format_value, check_polyaxonfile):
        self.runner.invoke(check, ["--version"])
        assert check_polyaxonfile.call_count == 1
        assert decorate_format_value.call_count == 1
