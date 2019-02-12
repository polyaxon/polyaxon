# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import job as job_events
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorJobTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.job = JobFactory(project=ProjectFactory())

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_created(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=job_events.JOB_CREATED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_updated(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=job_events.JOB_UPDATED,
                       instance=self.job,
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
    def test_job_started(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=job_events.JOB_STARTED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_started_triggered(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=job_events.JOB_STARTED_TRIGGERED,
                       instance=self.job,
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
    def test_job_cleaned_triggered(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=job_events.JOB_CLEANED_TRIGGERED,
                       instance=self.job,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 0
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_deleted(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=job_events.JOB_DELETED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_triggered_deleted(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=job_events.JOB_DELETED_TRIGGERED,
                       instance=self.job,
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
    def test_job_stopped(self,
                         activitylogs_record,
                         tracker_record,
                         notifier_record,
                         executor_record):
        auditor.record(event_type=job_events.JOB_STOPPED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_stopped_triggered(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=job_events.JOB_STOPPED_TRIGGERED,
                       instance=self.job,
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
    def test_job_viewed(self,
                        activitylogs_record,
                        tracker_record,
                        notifier_record,
                        executor_record):
        auditor.record(event_type=job_events.JOB_VIEWED,
                       instance=self.job,
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
    def test_job_archived(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record,
                          executor_record):
        auditor.record(event_type=job_events.JOB_ARCHIVED,
                       instance=self.job,
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
    def test_job_restored(self,
                          activitylogs_record,
                          tracker_record,
                          notifier_record,
                          executor_record):
        auditor.record(event_type=job_events.JOB_RESTORED,
                       instance=self.job,
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
    def test_job_bookmarked(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record,
                            executor_record):
        auditor.record(event_type=job_events.JOB_BOOKMARKED,
                       instance=self.job,
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
    def test_job_unbookmarked(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=job_events.JOB_UNBOOKMARKED,
                       instance=self.job,
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
    def test_job_new_status(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record,
                            executor_record):
        auditor.record(event_type=job_events.JOB_NEW_STATUS,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_failed(self,
                        activitylogs_record,
                        tracker_record,
                        notifier_record,
                        executor_record):
        auditor.record(event_type=job_events.JOB_FAILED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_succeeded(self,
                           activitylogs_record,
                           tracker_record,
                           notifier_record,
                           executor_record):
        auditor.record(event_type=job_events.JOB_SUCCEEDED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_done(self,
                      activitylogs_record,
                      tracker_record,
                      notifier_record,
                      executor_record):
        auditor.record(event_type=job_events.JOB_DONE,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_logs_viewed_triggered(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=job_events.JOB_LOGS_VIEWED,
                       instance=self.job,
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
    def test_job_restarted_triggered(self,
                                     activitylogs_record,
                                     tracker_record,
                                     notifier_record,
                                     executor_record):
        auditor.record(event_type=job_events.JOB_RESTARTED_TRIGGERED,
                       instance=self.job,
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
    def test_job_statuses_viewed_triggered(self,
                                           activitylogs_record,
                                           tracker_record,
                                           notifier_record,
                                           executor_record):
        auditor.record(event_type=job_events.JOB_STATUSES_VIEWED,
                       instance=self.job,
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
    def test_job_outputs_downloaded(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=job_events.JOB_OUTPUTS_DOWNLOADED,
                       instance=self.job,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
