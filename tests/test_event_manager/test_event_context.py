from unittest.mock import MagicMock

import pytest

from event_manager import event_context
from event_manager.event import Attribute, Event
from event_manager.event_context import EventContextSpec
from libs.unique_urls import (
    get_experiment_group_url,
    get_experiment_url,
    get_job_url,
    get_project_url
)
from tests.utils import BaseTest


@pytest.mark.events_mark
class TestEventContext(BaseTest):
    DISABLE_RUNNER = True

    def test_get_event_subject(self):
        assert event_context.get_event_subject('foo.bar') == 'foo'
        assert event_context.get_event_subject('foo.bar.moo') == 'foo'

    def test_get_event_action(self):
        assert event_context.get_event_action('foo.bar') == 'bar'
        assert event_context.get_event_action('foo.bar.moo') == 'bar'

    def test_get_event_actor_context(self):
        class DummyEvent1(Event):
            event_type = 'dummy.event'
            attributes = (
                Attribute('attr1'),
            )

        class DummyObject1(object):
            attr1 = 'test'

        obj = DummyObject1()
        event = DummyEvent1.from_instance(obj)
        assert event_context.get_event_actor_context(event=event) is None

        class DummyEvent2(Event):
            event_type = 'dummy.event'
            actor_name = 'actor_name'
            attributes = (
                Attribute('attr1'),
                Attribute('actor_name'),
            )

        class DummyObject2(object):
            attr1 = 'test'
            actor_name = 'test'

        obj = DummyObject2()
        event = DummyEvent2.from_instance(obj)
        event_spec = EventContextSpec('test', '/test', None)
        assert event_context.get_event_actor_context(event=event) == event_spec

    def test_get_event_object_context(self):
        mock_object = MagicMock()

        event_spec = EventContextSpec(None, None, None)
        assert event_context.get_event_object_context(None, 'event_type') == event_spec

        # Experiment
        mock_object.id = 1
        mock_object.unique_name = 'user.project.1'
        event_spec = EventContextSpec(mock_object.unique_name,
                                      get_experiment_url(mock_object.unique_name),
                                      1)
        assert event_context.get_event_object_context(mock_object, 'experiment') == event_spec

        # Experiment inside group
        mock_object.unique_name = 'user.project.2.1'
        event_spec = EventContextSpec(mock_object.unique_name,
                                      get_experiment_url(mock_object.unique_name),
                                      1)
        assert event_context.get_event_object_context(mock_object, 'experiment') == event_spec

        # Experiment group
        mock_object.unique_name = 'user.project.1'
        event_spec = EventContextSpec(mock_object.unique_name,
                                      get_experiment_group_url(mock_object.unique_name),
                                      1)
        assert event_context.get_event_object_context(mock_object, 'experiment_group') == event_spec

        # Job
        mock_object.unique_name = 'user.project.1'
        event_spec = EventContextSpec(mock_object.unique_name,
                                      get_job_url(mock_object.unique_name),
                                      1)
        assert event_context.get_event_object_context(mock_object, 'job') == event_spec

        # Project
        mock_object.unique_name = 'user.project'
        event_spec = EventContextSpec(mock_object.unique_name,
                                      get_project_url(mock_object.unique_name),
                                      1)
        assert event_context.get_event_object_context(mock_object, 'project') == event_spec
