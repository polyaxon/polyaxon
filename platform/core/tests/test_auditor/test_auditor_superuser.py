# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from events.registry import superuser as superuser_events
from tests.test_auditor.utils import AuditorBaseTest


@pytest.mark.auditor_mark
class AuditorSuperUserTest(AuditorBaseTest):
    """Testing subscribed events"""
    EVENTS = superuser_events.EVENTS

    def setUp(self):
        super().setUp()
        self.tested_events = {
            superuser_events.SUPERUSER_ROLE_GRANTED,
            superuser_events.SUPERUSER_ROLE_REVOKED,
        }

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_superuser_granted(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=superuser_events.SUPERUSER_ROLE_GRANTED,
                       id=2,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_superuser_revoked(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=superuser_events.SUPERUSER_ROLE_REVOKED,
                       id=2,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0


del AuditorBaseTest
