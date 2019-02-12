# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import build_job as build_job_events
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorBuildJobTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        self.build_job = BuildJobFactory(project=ProjectFactory())
        super().setUp()

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_created(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_CREATED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_updated(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_UPDATED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_started(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_started_triggered(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED_TRIGGERED,
                       instance=self.build_job,
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
    def test_build_job_deleted(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_DELETED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_triggered_deleted(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_DELETED_TRIGGERED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_stopped(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_stopped_triggered(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED_TRIGGERED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_cleaned_triggered(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_CLEANED_TRIGGERED,
                       instance=self.build_job)

        assert tracker_record.call_count == 0
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_viewed(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_VIEWED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_archived(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_ARCHIVED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_restored(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_RESTORED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_bookmarked(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_BOOKMARKED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_unbookmarked(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_UNBOOKMARKED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_new_status(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_NEW_STATUS,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_failed(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_FAILED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_succeeded(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_SUCCEEDED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_done(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record,
                            executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_DONE,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_logs_viewed_triggered(self,
                                             activitylogs_record,
                                             tracker_record,
                                             notifier_record,
                                             executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_LOGS_VIEWED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_statuses_viewed_triggered(self,
                                                 activitylogs_record,
                                                 tracker_record,
                                                 notifier_record,
                                                 executor_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STATUSES_VIEWED,
                       instance=self.build_job,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
