# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import superuser as superuser_events
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorSuperUserTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    @patch('executor.service.ExecutorService.record_event')
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

    @patch('executor.service.ExecutorService.record_event')
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
