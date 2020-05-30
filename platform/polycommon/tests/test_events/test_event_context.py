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
from unittest.mock import MagicMock

from polycommon import user_system
from polycommon.events import event_context
from polycommon.events.event import Attribute, Event
from polycommon.events.event_context import EventItemContextSpec
from polycommon.unique_urls import get_project_url, get_run_url


class TestEventContext(TestCase):
    def test_get_event_subject(self):
        assert event_context.get_event_subject("foo.bar") == "foo"
        assert event_context.get_event_subject("foo.bar.moo") == "foo"

    def test_get_event_action(self):
        assert event_context.get_event_action("foo.bar") == "bar"
        assert event_context.get_event_action("foo.bar.moo") == "bar"

    def test_get_event_actor_context(self):
        class DummyEvent1(Event):
            event_type = "dummy.event"
            attributes = (Attribute("attr1"),)

        class DummyObject1:
            attr1 = "test"

        obj = DummyObject1()
        event = DummyEvent1.from_instance(obj)
        assert event_context.get_event_actor_context(event=event) is None

        class DummyEvent2(Event):
            event_type = "dummy.event"
            actor = True
            attributes = (Attribute("attr1"),)

        class DummyObject2:
            attr1 = "test"
            actor_name = "test"
            actor_id = 1

        obj = DummyObject2()
        event = DummyEvent2.from_instance(obj)
        event_spec = EventItemContextSpec("test", "/test", None)
        assert event_context.get_event_actor_context(event=event) == event_spec

        obj.actor_name = user_system.USER_SYSTEM_NAME
        event = DummyEvent2.from_instance(obj)
        event_spec = EventItemContextSpec(user_system.USER_SYSTEM_NAME, "/", None)
        assert event_context.get_event_actor_context(event=event) == event_spec

    def test_get_event_object_context(self):
        mock_object = MagicMock(id=1)

        event_spec = EventItemContextSpec(None, None, None)
        assert event_context.get_event_object_context(None, "event_type") == event_spec

        # Run
        mock_object.unique_name = "user.project.1"
        event_spec = EventItemContextSpec(
            mock_object.unique_name,
            "app{}".format(get_run_url(mock_object.unique_name)),
            1,
        )
        assert event_context.get_event_object_context(mock_object, "run") == event_spec

        # Project
        mock_object.unique_name = "user.project"
        event_spec = EventItemContextSpec(
            mock_object.unique_name,
            "app{}".format(get_project_url(mock_object.unique_name)),
            1,
        )
        assert (
            event_context.get_event_object_context(mock_object, "project") == event_spec
        )
