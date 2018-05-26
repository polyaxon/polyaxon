from __future__ import absolute_import

import pytest

from event_manager.event_manager import EventManager
from event_manager.events.cluster import ClusterCreatedEvent, ClusterUpdatedEvent
from tests.utils import BaseTest


@pytest.mark.events
class TestEventManager(BaseTest):
    def setUp(self):
        self.manager = EventManager()

    def test_subscribe(self):
        # pylint:disable=len-as-condition
        assert len(self.manager.state) == 0
        self.manager.subscribe(ClusterCreatedEvent)
        assert len(self.manager.state) == 1
        assert ClusterCreatedEvent.event_type in self.manager.state
        assert self.manager.state[ClusterCreatedEvent.event_type] == ClusterCreatedEvent

        # Adding the same event
        self.manager.subscribe(ClusterCreatedEvent)
        assert len(self.manager.state) == 1

        # Adding new event
        self.manager.subscribe(ClusterUpdatedEvent)
        assert len(self.manager.state) == 2

        # Adding new event with same event type
        class DummyEvent(ClusterCreatedEvent):
            pass

        with self.assertRaises(AssertionError):
            self.manager.subscribe(DummyEvent)

    def test_knows(self):
        assert self.manager.knows(event_type=ClusterCreatedEvent.event_type) is False
        self.manager.subscribe(ClusterCreatedEvent)
        assert self.manager.knows(event_type=ClusterCreatedEvent.event_type) is True

        # Adding same event
        self.manager.subscribe(ClusterCreatedEvent)
        assert self.manager.knows(event_type=ClusterCreatedEvent.event_type) is True

        # New event
        assert self.manager.knows(ClusterUpdatedEvent) is False
        self.manager.subscribe(ClusterUpdatedEvent)
        assert self.manager.knows(event_type=ClusterCreatedEvent.event_type) is True

    def test_get(self):
        assert self.manager.get(event_type=ClusterCreatedEvent.event_type) is None
        self.manager.subscribe(ClusterCreatedEvent)
        assert self.manager.get(event_type=ClusterCreatedEvent.event_type) == ClusterCreatedEvent
