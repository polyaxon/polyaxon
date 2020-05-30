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

from unittest import TestCase

from polyaxon import types
from polycommon.conf.exceptions import ConfException
from polycommon.conf.handlers.env_handler import EnvConfHandler
from polycommon.options.option import Option, OptionScope, OptionStores


class DummyEnvOption(Option):
    key = "FOO_BAR1"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.ENV
    typing = types.INT
    default = None
    options = None


class DummyOptionalDefaultEnvOption(Option):
    key = "FOO_BAR2"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.ENV
    typing = types.STR
    default = "default_env"
    options = None


class DummyNonOptionalEnvOption(Option):
    key = "FOO_BAR3"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.ENV
    typing = types.INT
    default = None
    options = None


class DummySecretEnvOption(Option):
    key = "FOO_BAR4"
    scope = OptionScope.GLOBAL
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.ENV
    typing = types.INT
    default = None
    options = None


class TestClusterOptionsHandler(TestCase):
    def setUp(self):
        super().setUp()
        self.env_options_handler = EnvConfHandler()

    def test_get_default_value(self):
        assert self.env_options_handler.get(DummyEnvOption) is None
        assert (
            self.env_options_handler.get(DummyOptionalDefaultEnvOption) == "default_env"
        )
        with self.assertRaises(ConfException):
            self.env_options_handler.get(DummyNonOptionalEnvOption)
        with self.assertRaises(ConfException):
            self.env_options_handler.get(DummySecretEnvOption)

    def test_set_get_delete_value(self):
        self.env_options_handler.set(DummyEnvOption, 123)
        self.env_options_handler.set(DummyOptionalDefaultEnvOption, 123)
        self.env_options_handler.set(DummyNonOptionalEnvOption, 123)
        self.env_options_handler.set(DummySecretEnvOption, 123)

        assert self.env_options_handler.get(DummyEnvOption) == 123
        assert self.env_options_handler.get(DummyOptionalDefaultEnvOption) == "123"
        assert self.env_options_handler.get(DummyNonOptionalEnvOption) == 123
        assert self.env_options_handler.get(DummySecretEnvOption) == 123

        self.env_options_handler.delete(DummyEnvOption)
        self.env_options_handler.delete(DummyOptionalDefaultEnvOption)
        self.env_options_handler.delete(DummyNonOptionalEnvOption)
        self.env_options_handler.delete(DummySecretEnvOption)

        assert self.env_options_handler.get(DummyEnvOption) is None
        assert (
            self.env_options_handler.get(DummyOptionalDefaultEnvOption) == "default_env"
        )
        with self.assertRaises(ConfException):
            self.env_options_handler.get(DummyNonOptionalEnvOption)
        with self.assertRaises(ConfException):
            self.env_options_handler.get(DummySecretEnvOption)
