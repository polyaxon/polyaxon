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

from django.conf import settings

from polycommon.options.exceptions import OptionException
from polycommon.options.feature import Feature
from polycommon.options.option import NAMESPACE_DB_OPTION_MARKER, OptionStores


class DummyFeature(Feature):
    pass


class TestFeature(TestCase):
    def test_feature_default_store(self):
        assert DummyFeature.store == OptionStores(settings.STORE_OPTION)

    def test_feature_marker(self):
        assert DummyFeature.get_marker() == NAMESPACE_DB_OPTION_MARKER

    def test_parse_key_wtong_namespace(self):
        DummyFeature.key = "FOO"

        with self.assertRaises(OptionException):
            DummyFeature.parse_key()

        DummyFeature.key = "FOO:BAR"

        with self.assertRaises(OptionException):
            DummyFeature.parse_key()

    def test_parse_key_without_namespace(self):
        DummyFeature.key = "FEATURES:FOO"

        assert DummyFeature.parse_key() == (None, "FOO")

    def test_parse_key_with_namespace(self):
        DummyFeature.key = "FEATURES:FOO:BAR"

        assert DummyFeature.parse_key() == ("FOO", "BAR")
