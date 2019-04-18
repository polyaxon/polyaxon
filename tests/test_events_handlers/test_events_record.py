from unittest.mock import patch

import pytest

from events_handlers.tasks.record import events_log, events_notify, events_track
from tests.base.case import BaseTest


@pytest.mark.events_heandlers_mark
class BaseTestEventsHandling(BaseTest):
    def test_events_notify(self):
        with patch('auditor.notify') as mock_fct:
            events_notify(None)

        self.assertEqual(mock_fct.call_count, 1)

    def test_events_log(self):
        with patch('auditor.log') as mock_fct:
            events_log(None)

        self.assertEqual(mock_fct.call_count, 1)

    def test_events_track(self):
        with patch('auditor.track') as mock_fct:
            events_track(None)

        self.assertEqual(mock_fct.call_count, 1)
