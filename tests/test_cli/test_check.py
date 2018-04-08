# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from polyaxon_cli.cli.check import check
from tests.test_cli.utils import BaseCommandTestCase


class TestCheck(BaseCommandTestCase):
    @patch('polyaxon_cli.cli.check.check_polyaxonfile')
    def test_check_file(self, check_polyaxonfile):
        self.runner.invoke(check)
        assert check_polyaxonfile.call_count == 1

    @patch('polyaxon_cli.cli.check.check_polyaxonfile')
    @patch('polyaxon_cli.cli.check.click.echo')
    def test_check_file_all(self, echo, check_polyaxonfile):
        self.runner.invoke(check, ['--all'])
        assert check_polyaxonfile.call_count == 1
        assert echo.call_count == 1

    @patch('polyaxon_cli.cli.check.check_polyaxonfile')
    @patch('polyaxon_cli.cli.check.Printer.decorate_format_value')
    def test_check_file_version(self, decorate_format_value, check_polyaxonfile):
        self.runner.invoke(check, ['--version'])
        assert check_polyaxonfile.call_count == 1
        assert decorate_format_value.call_count == 1

    @patch('polyaxon_cli.cli.check.check_polyaxonfile')
    @patch('polyaxon_cli.cli.check.Printer.decorate_format_value')
    def test_check_file_run_type(self, decorate_format_value, check_polyaxonfile):
        self.runner.invoke(check, ['--run-type'])
        assert check_polyaxonfile.call_count == 1
        assert decorate_format_value.call_count == 1

    @patch('polyaxon_cli.cli.check.check_polyaxonfile')
    @patch('polyaxon_cli.cli.check.Printer.decorate_format_value')
    def test_check_file_project(self, decorate_format_value, check_polyaxonfile):
        self.runner.invoke(check, ['--project'])
        assert check_polyaxonfile.call_count == 1
        assert decorate_format_value.call_count == 1
