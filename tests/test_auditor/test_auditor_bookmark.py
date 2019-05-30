# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from events.registry import bookmark as bookmarks_events
from tests.test_auditor.utils import AuditorBaseTest


@pytest.mark.auditor_mark
class AuditorBookmarksTest(AuditorBaseTest):
    """Testing subscribed events"""
    EVENTS = bookmarks_events.EVENTS

    def setUp(self):
        super().setUp()
        self.tested_events = {
            bookmarks_events.BOOKMARK_BUILD_JOBS_VIEWED,
            bookmarks_events.BOOKMARK_JOBS_VIEWED,
            bookmarks_events.BOOKMARK_EXPERIMENTS_VIEWED,
            bookmarks_events.BOOKMARK_EXPERIMENT_GROUPS_VIEWED,
            bookmarks_events.BOOKMARK_PROJECTS_VIEWED,
        }

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_bookmarks_viewed(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=bookmarks_events.BOOKMARK_BUILD_JOBS_VIEWED,
                       actor_id=1,
                       actor_name='foo',
                       id=2)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_bookmarks_viewed(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=bookmarks_events.BOOKMARK_JOBS_VIEWED,
                       actor_id=1,
                       actor_name='foo',
                       id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_bookmarks_viewed(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=bookmarks_events.BOOKMARK_EXPERIMENTS_VIEWED,
                       actor_id=1,
                       actor_name='foo',
                       id=2)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_bookmarks_viewed(self,
                                               activitylogs_record,
                                               tracker_record,
                                               notifier_record,
                                               executor_record):
        auditor.record(event_type=bookmarks_events.BOOKMARK_EXPERIMENT_GROUPS_VIEWED,
                       actor_id=1,
                       actor_name='foo',
                       id=2)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_bookmarks_viewed(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=bookmarks_events.BOOKMARK_PROJECTS_VIEWED,
                       actor_id=1,
                       actor_name='foo',
                       id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0


del AuditorBaseTest
