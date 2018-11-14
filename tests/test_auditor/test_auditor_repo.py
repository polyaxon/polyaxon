# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import activitylogs
import auditor
import notifier
import tracker

from event_manager.events import repo as repo_events
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorRepoTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_RUNNER = True

    def setUp(self):
        self.project = RepoFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        notifier.validate()
        notifier.setup()
        super().setUp()

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_repo_created(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record):
        auditor.record(event_type=repo_events.REPO_CREATED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_repo_downloaded(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record):
        auditor.record(event_type=repo_events.REPO_DOWNLOADED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_repo_new_commit(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record):
        auditor.record(event_type=repo_events.REPO_NEW_COMMIT,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
