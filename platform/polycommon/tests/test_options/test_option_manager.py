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

from polycommon.options.option_manager import OptionManager
from polycommon.options.registry.core import CeleryBrokerUrl, Logging


class TestOptionManager(TestCase):
    def setUp(self):
        self.manager = OptionManager()
        super().setUp()

    def test_subscribe(self):
        self.assertEqual(len(self.manager.state), 0)
        self.manager.subscribe(CeleryBrokerUrl)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1
        assert CeleryBrokerUrl.key in self.manager.state
        assert self.manager.state[CeleryBrokerUrl.key] == CeleryBrokerUrl

        # Adding the same event
        self.manager.subscribe(CeleryBrokerUrl)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1

        # Adding new event
        self.manager.subscribe(Logging)
        assert len(self.manager.state) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.keys) == 2
        assert len(self.manager.values) == 2

        # Adding new event with same event type
        class DummyEvent(Logging):
            pass

        with self.assertRaises(AssertionError):
            self.manager.subscribe(DummyEvent)

    def test_knows(self):
        assert self.manager.knows(key=CeleryBrokerUrl.key) is False
        self.manager.subscribe(CeleryBrokerUrl)
        assert self.manager.knows(key=CeleryBrokerUrl.key) is True

        # Adding same event
        self.manager.subscribe(CeleryBrokerUrl)
        assert self.manager.knows(key=CeleryBrokerUrl.key) is True

        # New event
        assert self.manager.knows(Logging) is False
        self.manager.subscribe(Logging)
        assert self.manager.knows(key=Logging.key) is True

    def test_get(self):
        assert self.manager.get(key=CeleryBrokerUrl.key) is None
        self.manager.subscribe(CeleryBrokerUrl)
        assert self.manager.get(key=CeleryBrokerUrl.key) == CeleryBrokerUrl
