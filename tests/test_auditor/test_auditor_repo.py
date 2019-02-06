# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import repo as repo_events
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorRepoTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        self.project = RepoFactory()
        super().setUp()

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_repo_created(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record,
                          executor_record):
        auditor.record(event_type=repo_events.REPO_CREATED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo',
                       external=True)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_repo_downloaded(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record,
                             executor_record):
        auditor.record(event_type=repo_events.REPO_DOWNLOADED,
                       instance=self.project,
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
    def test_repo_new_commit(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record,
                             executor_record):
        auditor.record(event_type=repo_events.REPO_NEW_COMMIT,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
