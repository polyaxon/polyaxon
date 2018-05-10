# pylint:disable=ungrouped-imports

from unittest.mock import patch

import activitylogs
import auditor
import tracker

from event_manager.events import user as user_events
from factories.factory_users import UserFactory
from tests.utils import BaseTest


class AuditorUserTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.user = UserFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorUserTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_registered(self, tracker_record, activitylogs_record):
        auditor.record(event_type=user_events.USER_REGISTERED,
                       instance=self.user)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_updated(self, tracker_record, activitylogs_record):
        auditor.record(event_type=user_events.USER_UPDATED,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_activated(self, tracker_record, activitylogs_record):
        auditor.record(event_type=user_events.USER_ACTIVATED,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_deleted(self, tracker_record, activitylogs_record):
        auditor.record(event_type=user_events.USER_DELETED,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
