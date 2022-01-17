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
from unittest.mock import MagicMock
from uuid import uuid1

from polycommon import user_system
from polycommon.events.event import Attribute, Event
from polycommon.events.registry import run
from polycommon.json_utils import loads


class TestEvents(TestCase):
    def test_serialize(self):
        class DummyEvent(Event):
            event_type = "dummy.event"
            attributes = (Attribute("attr1"),)

        event = DummyEvent(attr1="test")
        event_serialized = event.serialize(dumps=False)
        assert event_serialized["type"] == "dummy.event"
        assert event_serialized["uuid"] is not None
        assert event_serialized["timestamp"] is not None
        assert event_serialized["data"]["attr1"] == "test"

        event_serialized_dump = event.serialize(dumps=True)
        assert event_serialized == loads(event_serialized_dump)

    def test_serialize_with_instance(self):
        instance = MagicMock(instance_id=1)
        event = run.RunSucceededEvent.from_instance(
            instance=instance, actor_id=1, actor_name="user"
        )
        event.serialize(dumps=False, include_instance_info=True)

    def test_from_event_data(self):
        instance = MagicMock(ref_id=None)
        event = run.RunSucceededEvent.from_instance(
            instance=instance,
            actor_id=1,
            actor_name="user",
            project_id=1,
            project_name="project",
            project_owner_id=1,
            project_owner_name="owner",
        )
        assert event.ref_id is None
        event_serialized = event.serialize(dumps=False, include_instance_info=True)
        assert event_serialized.get("ref_id") is None
        new_event = run.RunSucceededEvent.from_event_data(event_data=event_serialized)
        assert new_event.serialize(include_instance_info=True) == event_serialized

        # Add ref id
        event.ref_id = uuid1()
        event_serialized = event.serialize(dumps=False, include_instance_info=True)
        assert event_serialized["ref_id"] == event.ref_id.hex
        new_event = run.RunSucceededEvent.from_event_data(event_data=event_serialized)
        assert new_event.ref_id == event.ref_id
        assert new_event.serialize(include_instance_info=True) == event_serialized

    def test_get_value_from_instance(self):
        class DummyEvent(Event):
            event_type = "dummy.event"

        class SimpleObject:
            attr1 = "test"

        class ComposedObject:
            attr2 = SimpleObject()

        value = DummyEvent.get_value_from_instance(
            attr="attr1", instance=SimpleObject()
        )
        assert value == "test"

        value = DummyEvent.get_value_from_instance(
            attr="attr2", instance=SimpleObject()
        )
        assert value is None

        value = DummyEvent.get_value_from_instance(
            attr="attr2.attr1", instance=ComposedObject()
        )
        assert value == "test"

        value = DummyEvent.get_value_from_instance(
            attr="attr2.attr3", instance=ComposedObject()
        )
        assert value is None

        value = DummyEvent.get_value_from_instance(
            attr="attr2.attr1.attr3", instance=ComposedObject()
        )
        assert value is None

        value = DummyEvent.get_value_from_instance(
            attr="attr2.attr4.attr3", instance=SimpleObject()
        )
        assert value is None

    def test_from_instance_simple_event(self):
        class DummyEvent(Event):
            event_type = "dummy.event"
            attributes = (Attribute("attr1"),)

        class DummyObject:
            attr1 = "test"

        obj = DummyObject()
        event = DummyEvent.from_instance(obj)
        event_serialized = event.serialize(dumps=False)
        assert event_serialized["type"] == "dummy.event"
        assert event_serialized["uuid"] is not None
        assert event_serialized["timestamp"] is not None
        assert event_serialized["data"]["attr1"] == "test"

    def test_from_instance_nested_event(self):
        class DummyEvent(Event):
            event_type = "dummy.event"
            attributes = (
                Attribute("attr1"),
                Attribute("attr2.attr3"),
                Attribute("attr2.attr4", is_required=False),
            )

        class DummyObject:
            class NestedObject:
                attr3 = "test2"

            attr1 = "test"
            attr2 = NestedObject()

        obj = DummyObject()
        event = DummyEvent.from_instance(obj)
        event_serialized = event.serialize(dumps=False)
        assert event_serialized["type"] == "dummy.event"
        assert event_serialized["uuid"] is not None
        assert event_serialized["timestamp"] is not None
        assert event_serialized["data"]["attr1"] == "test"
        assert event_serialized["data"]["attr2.attr3"] == "test2"
        assert event_serialized["data"]["attr2.attr4"] is None

    def test_actor(self):
        class DummyEvent1(Event):
            event_type = "dummy.event"
            actor = True
            attributes = (Attribute("attr1"),)

        class DummyEvent2(Event):
            event_type = "dummy.event"
            actor = True
            actor_id = "some_actor_id"
            actor_name = "some_actor_name"
            attributes = (Attribute("attr1"),)

        class DummyObject1:
            attr1 = "test"

        class DummyObject2:
            attr1 = "test"
            some_actor_id = 1
            some_actor_name = "foo"

        # Not providing actor_id raises
        obj = DummyObject1()
        with self.assertRaises(ValueError):
            DummyEvent1.from_instance(obj)

        # Providing actor_id and not actor_name raises
        with self.assertRaises(ValueError):
            DummyEvent1.from_instance(obj, actor_id=1)

        # Providing system actor id without actor_name does not raise
        event = DummyEvent1.from_instance(obj, actor_id=user_system.USER_SYSTEM_ID)
        assert event.data["actor_id"] == user_system.USER_SYSTEM_ID
        assert event.data["actor_name"] == user_system.USER_SYSTEM_NAME

        # Providing actor_id and actor_name does not raise
        event = DummyEvent1.from_instance(obj, actor_id=1, actor_name="foo")
        assert event.data["actor_id"] == 1
        assert event.data["actor_name"] == "foo"

        # Using an instance that has the actor properties
        obj2 = DummyObject2()
        event = DummyEvent2.from_instance(obj2)
        assert event.data["some_actor_id"] == 1
        assert event.data["some_actor_name"] == "foo"

        # Using an instance that has the actor properties and overriding the actor
        event = DummyEvent2.from_instance(
            obj2,
            some_actor_id=user_system.USER_SYSTEM_ID,
            some_actor_name=user_system.USER_SYSTEM_NAME,
        )
        assert event.data["some_actor_id"] == user_system.USER_SYSTEM_ID
        assert event.data["some_actor_name"] == user_system.USER_SYSTEM_NAME
