from unittest.mock import patch

import pytest

from checks.events import EventsCheck
from checks.results import Result
from tests.utils import BaseTest


@pytest.mark.checks_mark
class TestEventsHealthCheck(BaseTest):
    def test_events_is_healthy(self):
        results = EventsCheck.run()
        assert results['EVENTS'].is_healthy is True

    @patch('events_handlers.tasks.health.events_health.apply_async')
    def test_events_wrong_results(self, mock_health):
        mock_health.return_value.__enter__.return_value = None

        results = EventsCheck.run()
        assert results['EVENTS'].is_healthy is False
        assert results['EVENTS'].severity == Result.WARNING

    @patch('events_handlers.tasks.health.events_health.apply_async')
    def test_events_not_healthy(self, mock_health):
        mock_health.side_effect = Exception('Connection Refused')

        results = EventsCheck.run()
        assert results['EVENTS'].is_healthy is False
        assert results['EVENTS'].severity == Result.ERROR
