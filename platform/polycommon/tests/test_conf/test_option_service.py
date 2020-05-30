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

import os

from unittest import TestCase

from django.conf import settings

from polyaxon import types
from polycommon.conf.exceptions import ConfException
from polycommon.conf.service import ConfService
from polycommon.options.option import Option, OptionScope, OptionStores
from polycommon.options.option_manager import OptionManager


class DummySettingsService(ConfService):
    def __init__(self):
        self.options = set([])
        super().__init__()

    def get(self, key, check_cache=True, to_dict=False):
        self.options.add(key)
        return super().get(key, check_cache=check_cache, to_dict=to_dict)


class DummyEnvService(ConfService):
    def __init__(self):
        self.options = set([])
        super().__init__()

    def get(self, key, check_cache=True, to_dict=False):
        self.options.add(key)
        return super().get(key, check_cache=check_cache, to_dict=to_dict)


class DummySettingsOption(Option):
    key = "FOO_BAR"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class DummyOptionalDefaultSettingsOption(Option):
    key = "FOO_BAR2"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = "default_settings"
    options = None


class DummyNonOptionalSettingsOption(Option):
    key = "FOO_BAR2"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = types.STR
    default = None
    options = None


class DummyEnvOption(Option):
    key = "FOO_BAR"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.ENV
    typing = types.STR
    default = None
    options = None
    cache_ttl = 0


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
    key = "FOO_BAR2"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.ENV
    typing = types.STR
    default = None
    options = None


class DummyBoolEnvOption(Option):
    key = "BOOL_KEY"
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.ENV
    typing = types.BOOL
    default = True
    options = None


class TestConfService(TestCase):
    def setUp(self):
        super().setUp()
        self.settings_service = DummySettingsService()
        self.env_service = DummyEnvService()
        self.settings_service.option_manager = OptionManager()
        self.env_service.option_manager = OptionManager()
        self.settings_service.setup()
        self.env_service.setup()

    def test_can_handle(self):
        # Test handles only str event types
        assert self.settings_service.can_handle(key=1) is False

        # The service's manager did not subscribe to the event yet
        assert self.settings_service.can_handle(key=DummySettingsOption.key) is False

        # Subscribe to the event
        self.settings_service.option_manager.subscribe(DummySettingsOption)
        assert self.settings_service.can_handle(key=DummySettingsOption.key) is True

    def test_non_optional_settings(self):
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyNonOptionalSettingsOption.key)
        # Subscribe to the event
        self.settings_service.option_manager.subscribe(DummyNonOptionalSettingsOption)
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyNonOptionalSettingsOption.key)

    def test_non_optional_env(self):
        with self.assertRaises(ConfException):
            self.env_service.get(key=DummyNonOptionalEnvOption.key)
        # Subscribe to the event
        self.env_service.option_manager.subscribe(DummyNonOptionalEnvOption)
        with self.assertRaises(ConfException):
            self.env_service.get(key=DummyNonOptionalEnvOption.key)

    def test_optional_with_default_settings(self):
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyOptionalDefaultSettingsOption.key)
        # Subscribe to the event
        self.settings_service.option_manager.subscribe(
            DummyOptionalDefaultSettingsOption
        )
        assert (
            self.settings_service.get(key=DummyOptionalDefaultSettingsOption.key)
            == "default_settings"
        )

    def test_optional_with_default_env(self):
        with self.assertRaises(ConfException):
            self.env_service.get(key=DummyOptionalDefaultEnvOption.key)
        # Subscribe to the event
        self.env_service.option_manager.subscribe(DummyOptionalDefaultEnvOption)
        assert (
            self.env_service.get(key=DummyOptionalDefaultEnvOption.key) == "default_env"
        )

    def test_get_from_settings(self):
        settings.FOO_BAR = None
        # The service's manager did not subscribe to the event yet
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummySettingsOption.key)

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        # No entry in settings
        assert self.settings_service.get(key=DummySettingsOption.key) is None

        # Update settings
        settings.FOO_BAR = "foo"
        assert self.settings_service.get(key=DummySettingsOption.key) == "foo"

        # Get as option
        option_dict = DummySettingsOption.to_dict(value="foo")
        assert option_dict["value"] == "foo"
        assert (
            self.settings_service.get(key=DummySettingsOption.key, to_dict=True)
            == option_dict
        )

        assert len(self.settings_service.options) == 1
        option_key = self.settings_service.options.pop()
        assert option_key == DummySettingsOption.key

    def test_get_from_env(self):
        # The service's manager did not subscribe to the event yet
        with self.assertRaises(ConfException):
            self.env_service.get(key=DummyEnvOption.key)

        # Subscribe
        self.env_service.option_manager.subscribe(DummyEnvOption)

        # No entry in env
        assert self.env_service.get(key=DummyEnvOption.key) is None

        # Update settings does not change anything
        settings.FOO_BAR = "foo"
        assert self.env_service.get(key=DummyEnvOption.key) is None

        # Update env
        os.environ[DummyEnvOption.key] = "foo"
        assert self.env_service.get(key=DummyEnvOption.key) == "foo"

        # Get as option
        option_dict = DummyEnvOption.to_dict(value="foo")
        assert option_dict["value"] == "foo"
        assert self.env_service.get(key=DummyEnvOption.key, to_dict=True) == option_dict

        assert len(self.env_service.options) == 1
        option_key = self.env_service.options.pop()
        assert option_key == DummyEnvOption.key

        # Get bool options
        self.env_service.option_manager.subscribe(DummyBoolEnvOption)

        option_dict = DummyBoolEnvOption.to_dict(value=True)
        assert option_dict["value"] is True
        assert (
            self.env_service.get(key=DummyBoolEnvOption.key, to_dict=True)
            == option_dict
        )

        option_dict = DummyBoolEnvOption.to_dict(value=False)
        assert option_dict["value"] is False

        os.environ[DummyBoolEnvOption.key] = "false"
        assert (
            self.env_service.get(key=DummyBoolEnvOption.key, to_dict=True)
            == option_dict
        )

    def test_option_caching(self):
        os.environ.pop(DummyEnvOption.key, None)
        # Subscribe
        self.env_service.option_manager.subscribe(DummyEnvOption)

        # No entry in env
        assert self.env_service.get(key=DummyEnvOption.key) is None

        # Update env
        os.environ[DummyEnvOption.key] = "foo"
        assert self.env_service.get(key=DummyEnvOption.key) == "foo"

        # Cache is 0, changing the value should be reflected automatically
        os.environ[DummyEnvOption.key] = "bar"
        assert self.env_service.get(key=DummyEnvOption.key) == "bar"

        # Update caching ttl
        DummyEnvOption.cache_ttl = 10
        assert self.env_service.get(key=DummyEnvOption.key) == "bar"
        os.environ[DummyEnvOption.key] = "foo"
        assert self.env_service.get(key=DummyEnvOption.key) == "bar"
        assert self.env_service.get(key=DummyEnvOption.key, check_cache=False) == "foo"

        # Delete remove from cache
        DummyEnvOption.cache_ttl = 0
        self.env_service.delete(key=DummyEnvOption.key)
        assert self.env_service.get(key=DummyEnvOption.key) is None

        # Set new value
        os.environ[DummyEnvOption.key] = "foo"
        # Update caching ttl
        DummyEnvOption.cache_ttl = 0
        assert self.env_service.get(key=DummyEnvOption.key) == "foo"
        os.environ[DummyEnvOption.key] = "bar"
        assert self.env_service.get(key=DummyEnvOption.key) == "bar"
        os.environ[DummyEnvOption.key] = "foo"
        assert self.env_service.get(key=DummyEnvOption.key) == "foo"

    def test_setting_none_value_raises(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key="SOME_NEW_KEY", value=None)

        with self.assertRaises(ConfException):
            self.env_service.set(key="SOME_NEW_KEY", value=None)

    def test_setting_unknown_key_raises(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key="SOME_NEW_KEY", value="foo_bar")

        with self.assertRaises(ConfException):
            self.env_service.set(key="SOME_NEW_KEY", value="foo_bar")

    def test_cannot_set_keys_on_settings_backend(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key=DummySettingsOption.key, value="foo_bar")

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        with self.assertRaises(ConfException):
            self.settings_service.set(key=DummySettingsOption.key, value="foo_bar")

    def test_cannot_delete_keys_on_settings_backend(self):
        with self.assertRaises(ConfException):
            self.settings_service.delete(key=DummySettingsOption.key)

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        with self.assertRaises(ConfException):
            self.settings_service.delete(key=DummySettingsOption.key)
