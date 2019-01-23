import pytest

from event_manager.event_manager import EventManager
from event_manager.events.cluster import ClusterCreatedEvent, ClusterUpdatedEvent
from event_manager.events.experiment import (
    ExperimentCreatedEvent,
    ExperimentDeletedEvent,
    ExperimentViewedEvent
)
from tests.utils import BaseTest


@pytest.mark.events_mark
class TestEventManager(BaseTest):
    def setUp(self):
        self.manager = EventManager()
        super().setUp()

    def test_subscribe(self):
        self.assertEqual(len(self.manager.state), 0)
        self.manager.subscribe(ClusterCreatedEvent)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1
        assert ClusterCreatedEvent.event_type in self.manager.state
        assert self.manager.state[ClusterCreatedEvent.event_type] == ClusterCreatedEvent

        # Adding the same event
        self.manager.subscribe(ClusterCreatedEvent)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1

        # Adding new event
        self.manager.subscribe(ClusterUpdatedEvent)
        assert len(self.manager.state) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.keys) == 2
        assert len(self.manager.values) == 2

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

    def test_user_write_events(self):
        assert self.manager.user_write_events() == []
        self.manager.subscribe(ClusterCreatedEvent)
        assert self.manager.user_write_events() == []
        self.manager.subscribe(ExperimentViewedEvent)
        assert self.manager.user_write_events() == []
        self.manager.subscribe(ExperimentDeletedEvent)
        assert self.manager.user_write_events() == []
        self.manager.subscribe(ExperimentCreatedEvent)
        assert self.manager.user_write_events() == [ExperimentCreatedEvent.event_type]

    def test_user_view_events(self):
        assert self.manager.user_view_events() == []
        self.manager.subscribe(ClusterCreatedEvent)
        assert self.manager.user_view_events() == []
        self.manager.subscribe(ExperimentCreatedEvent)
        assert self.manager.user_view_events() == []
        self.manager.subscribe(ExperimentCreatedEvent)
        assert self.manager.user_view_events() == []
        self.manager.subscribe(ExperimentDeletedEvent)
        assert self.manager.user_view_events() == []
        self.manager.subscribe(ExperimentViewedEvent)
        assert self.manager.user_view_events() == [ExperimentViewedEvent.event_type]
