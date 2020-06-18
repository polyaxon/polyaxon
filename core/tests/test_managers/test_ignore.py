#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import mock_open, patch

import pytest

from tests.utils import BaseTestCase

from polyaxon.managers.ignore import IgnoreManager


@pytest.mark.managers_mark
class TestIgnoreManager(BaseTestCase):
    """Mock the config ignore file."""

    def test_default_props(self):
        assert IgnoreManager.is_global() is False
        assert IgnoreManager.IS_POLYAXON_DIR is False
        assert IgnoreManager.CONFIG_FILE_NAME == ".polyaxonignore"
        assert IgnoreManager.CONFIG is None

    @staticmethod
    def get_ignored(patterns):
        return [r.pattern for r in patterns if r.is_exclude]

    @staticmethod
    def get_whitelisted(patterns):
        return [r.pattern for r in patterns if not r.is_exclude]

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_ignored_lines(self, mock_file, _):
        configs = [
            ("foo.c", "foo.[dh]"),
            ("foo/foo.c", "/foo.c"),
            ("foo/foo.c", "/*.c"),
            ("foo/bar/", "/bar/"),
            ("foo/bar/", "foo/bar/*"),
            ("foo/bar", "foo?bar"),
        ]
        for (path, pattern) in configs:
            mock_file.return_value.__enter__.return_value = [pattern]
            patterns = IgnoreManager.get_config()
            self.assertEqual(
                (self.get_ignored(patterns), self.get_whitelisted(patterns)),
                ([pattern], []),
            )
            assert list(IgnoreManager.find_matching(path, patterns)) == []

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_whitelisted_lines(self, mock_file, _):
        configs = [
            ("foo.c", "*.c"),
            (".c", "*.c"),
            ("foo/foo.c", "*.c"),
            ("foo/foo.c", "foo.c"),
            ("foo.c", "/*.c"),
            ("foo.c", "/foo.c"),
            ("foo.c", "foo.c"),
            ("foo.c", "foo.[ch]"),
            ("foo/bar/bla.c", "foo/**"),
            ("foo/bar/bla/blie.c", "foo/**/blie.c"),
            ("foo/bar/bla.c", "**/bla.c"),
            ("bla.c", "**/bla.c"),
            ("foo/bar", "foo/**/bar"),
            ("foo/bla/bar", "foo/**/bar"),
            ("foo/bar/", "bar/"),
            ("foo/bar/", "bar"),
            ("foo/bar/something", "foo/bar/*"),
        ]
        for (path, pattern) in configs:
            mock_file.return_value.__enter__.return_value = [pattern]
            patterns = IgnoreManager.get_config()
            self.assertEqual(
                (self.get_ignored(patterns), self.get_whitelisted(patterns)),
                ([pattern], []),
            )
            assert len(list(IgnoreManager.find_matching(path, patterns))) == 1

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_ignores_commented_lines(self, mock_file, _):
        file_data = ["", "# comment", "", "*.py"]
        mock_file.return_value.__enter__.return_value = file_data

        patterns = IgnoreManager.get_config()
        self.assertEqual(
            (self.get_ignored(patterns), self.get_whitelisted(patterns)), (["*.py"], [])
        )

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_trims_slash_prefix_from_abs_paths(self, mock_file, _):
        file_data = ["/test", "!/ignore"]
        mock_file.return_value.__enter__.return_value = file_data

        patterns = IgnoreManager.get_config()
        self.assertEqual(
            (self.get_ignored(patterns), self.get_whitelisted(patterns)),
            (["/test"], ["/ignore"]),
        )

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_properly_interprets_whitelisted_globs(self, mock_file, _):
        file_data = ["", "# comment", "*.py", "!file1.py"]
        mock_file.return_value.__enter__.return_value = file_data

        patterns = IgnoreManager.get_config()
        self.assertEqual(
            (self.get_ignored(patterns), self.get_whitelisted(patterns)),
            (["*.py"], ["file1.py"]),
        )

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=False)
    def test_returns_two_empty_lists_if_file_is_not_present(self, _):
        patterns = IgnoreManager.get_config()
        self.assertEqual(patterns, [])

    @patch("polyaxon.managers.ignore.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_escaping_of_globs_that_start_with_reserved_chars(self, mock_file, _):
        file_data = ["", "# comment", "\#file1", "\!file2"]  # noqa
        mock_file.return_value.__enter__.return_value = file_data

        patterns = IgnoreManager.get_config()
        self.assertEqual(
            (self.get_ignored(patterns), self.get_whitelisted(patterns)),
            (["#file1", "!file2"], []),
        )
