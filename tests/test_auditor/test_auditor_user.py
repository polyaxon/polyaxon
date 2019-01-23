# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import user as user_events
from factories.factory_users import UserFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorUserTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        self.user = UserFactory()
        super().setUp()

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_registered(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record,
                             executor_record):
        auditor.record(event_type=user_events.USER_REGISTERED,
                       instance=self.user)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_updated(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record,
                          executor_record):
        auditor.record(event_type=user_events.USER_UPDATED,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_activated(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record,
                            executor_record):
        auditor.record(event_type=user_events.USER_ACTIVATED,
                       instance=self.user,
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
    def test_user_deleted(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record,
                          executor_record):
        auditor.record(event_type=user_events.USER_DELETED,
                       instance=self.user,
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
    def test_user_ldap(self,
                       activitylogs_record,
                       tracker_record,
                       notifier_record,
                       executor_record):
        auditor.record(event_type=user_events.USER_LDAP,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_github(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=user_events.USER_GITHUB,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_gitlab(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=user_events.USER_GITLAB,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_bitbucket(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record,
                            executor_record):
        auditor.record(event_type=user_events.USER_BITBUCKET,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_user_azure(self,
                        activitylogs_record,
                        tracker_record,
                        notifier_record,
                        executor_record):
        auditor.record(event_type=user_events.USER_AZURE,
                       instance=self.user,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
