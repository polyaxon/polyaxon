# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import mock_open, patch
from unittest import TestCase

from polyaxon_cli.managers.ignore import IgnoreManager


class TestIgnoreManager(TestCase):
    """Mock the config ignore file."""
    def test_default_props(self):
        assert IgnoreManager.IS_GLOBAL is False
        assert IgnoreManager.IS_POLYAXON_DIR is False
        assert IgnoreManager.CONFIG_FILE_NAME == '.polyaxonignore'
        assert IgnoreManager.CONFIG is None

    @patch('polyaxon_cli.managers.ignore.os.path.isfile', return_value=True)
    @patch('polyaxon_cli.managers.ignore.open', new_callable=mock_open)
    def test_ignores_commented_lines(self, mock_open, _):
        file_data = ['', '# comment', '', '*.py']
        mock_open.return_value.__iter__.return_value = file_data

        result = IgnoreManager.get_config()
        self.assertEqual(result, (['*.py'], []))

    @patch('polyaxon_cli.managers.ignore.os.path.isfile', return_value=True)
    @patch('polyaxon_cli.managers.ignore.open', new_callable=mock_open)
    def test_trims_slash_prefix_from_abs_paths(self, mock_open, _):
        file_data = ['/test', '!/ignore']
        mock_open.return_value.__iter__.return_value = file_data

        result = IgnoreManager.get_config()
        self.assertEqual(result, (['test'], ['ignore']))

    @patch('polyaxon_cli.managers.ignore.os.path.isfile', return_value=True)
    @patch('polyaxon_cli.managers.ignore.open', new_callable=mock_open)
    def test_properly_interprets_whitelisted_globs(self, mock_open, _):
        file_data = ['', '# comment', '*.py', '!file1.py']
        mock_open.return_value.__iter__.return_value = file_data

        result = IgnoreManager.get_config()
        self.assertEqual(result, (['*.py'], ['file1.py']))

    @patch('polyaxon_cli.managers.ignore.os.path.isfile', return_value=False)
    def test_returns_two_empty_lists_if_file_is_not_present(self, _):
        result = IgnoreManager.get_config()
        self.assertEqual(result, ([], []))

    @patch('polyaxon_cli.managers.ignore.os.path.isfile', return_value=True)
    @patch('polyaxon_cli.managers.ignore.open', new_callable=mock_open)
    def test_escaping_of_globs_that_start_with_reserved_chars(self, mock_open, _):
        file_data = ['', '# comment', '\#file1', '\!file2']
        mock_open.return_value.__iter__.return_value = file_data

        result = IgnoreManager.get_config()
        self.assertEqual(result, (['#file1', '!file2'], []))
