#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from unittest import TestCase

from polycommon.options.exceptions import OptionException
from polycommon.options.option import (
    NAMESPACE_DB_CONFIG_MARKER,
    NAMESPACE_DB_OPTION_MARKER,
    NAMESPACE_ENV_MARKER,
    NAMESPACE_SETTINGS_MARKER,
    Option,
    OptionStores,
)


class DummyOption(Option):
    pass


class TestOption(TestCase):
    def test_option_marker(self):
        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.get_marker() == NAMESPACE_DB_OPTION_MARKER

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.get_marker() == NAMESPACE_DB_CONFIG_MARKER

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.get_marker() == NAMESPACE_SETTINGS_MARKER

        DummyOption.store = OptionStores.ENV
        assert DummyOption.get_marker() == NAMESPACE_ENV_MARKER

    def test_parse_key_without_namespace(self):
        DummyOption.key = "FOO"

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, "FOO")

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, "FOO")

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, "FOO")

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, "FOO")

    def test_parse_key_with_namespace(self):
        DummyOption.key = "FOO:BAR"

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == ("FOO", "BAR")

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, "FOO:BAR")

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, "FOO:BAR")

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == ("FOO", "BAR")

        DummyOption.key = "FOO__BAR"

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, "FOO__BAR")

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == ("FOO", "BAR")

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == ("FOO", "BAR")

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, "FOO__BAR")

    def test_parse_key_wrong_namespace(self):
        DummyOption.key = "FOO:BAR:MOO"

        DummyOption.store = OptionStores.DB_OPTION
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.ENV
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, "FOO:BAR:MOO")

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, "FOO:BAR:MOO")

        DummyOption.key = "FOO__BAR__MOO"

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, "FOO__BAR__MOO")

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, "FOO__BAR__MOO")

        DummyOption.store = OptionStores.DB_CONFIG
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.SETTINGS
        with self.assertRaises(OptionException):
            DummyOption.parse_key()
