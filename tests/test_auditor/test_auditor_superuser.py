# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import superuser as superuser_events
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorSuperUserTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorSuperUserTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_superuser_granted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=superuser_events.SUPERUSER_ROLE_GRANTED,
                       id=2,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_superuser_revoked(self, activitylogs_record, tracker_record):
        auditor.record(event_type=superuser_events.SUPERUSER_ROLE_REVOKED,
                       id=2,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
