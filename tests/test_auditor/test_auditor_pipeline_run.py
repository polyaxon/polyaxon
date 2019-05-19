# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import pipeline_run as pipeline_run_events
from factories.factory_pipelines import PipelineRunFactory
from tests.test_auditor.utils import AuditorBaseTest


@pytest.mark.auditor_mark
class AuditorPipelineRunTest(AuditorBaseTest):
    """Testing subscribed events"""
    EVENTS = pipeline_run_events.EVENTS

    def setUp(self):
        super().setUp()
        self.pipeline_run = PipelineRunFactory()
        self.tested_events = {
            pipeline_run_events.PIPELINE_RUN_CREATED,
            pipeline_run_events.PIPELINE_RUN_UPDATED,
            pipeline_run_events.PIPELINE_RUN_DELETED,
            pipeline_run_events.PIPELINE_RUN_CLEANED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_VIEWED,
            pipeline_run_events.PIPELINE_RUN_ARCHIVED,
            pipeline_run_events.PIPELINE_RUN_RESTORED,
            pipeline_run_events.PIPELINE_RUN_DELETED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_STOPPED,
            pipeline_run_events.PIPELINE_RUN_STOPPED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_SKIPPED,
            pipeline_run_events.PIPELINE_RUN_SKIPPED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_RESUMED,
            pipeline_run_events.PIPELINE_RUN_RESTARTED,
            pipeline_run_events.PIPELINE_RUN_RESTARTED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_RESUMED_TRIGGERED,
            pipeline_run_events.PIPELINE_RUN_NEW_STATUS,
            pipeline_run_events.PIPELINE_RUN_SUCCEEDED,
            pipeline_run_events.PIPELINE_RUN_FAILED,
            pipeline_run_events.PIPELINE_RUN_DONE,
        }

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_created(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_CREATED,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_updated(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_UPDATED,
                       instance=self.pipeline_run,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_deleted(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_DELETED,
                       instance=self.pipeline_run)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_cleaned_triggered(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_CLEANED_TRIGGERED,
                       instance=self.pipeline_run)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_viewed(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_VIEWED,
                       instance=self.pipeline_run,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_archived(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_ARCHIVED,
                       instance=self.pipeline_run,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_restored(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_RESTORED,
                       instance=self.pipeline_run,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_triggered_deleted(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_DELETED_TRIGGERED,
                       instance=self.pipeline_run,
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
    def test_pipeline_run_stopped(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_STOPPED,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_stopped_triggered(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_STOPPED_TRIGGERED,
                       instance=self.pipeline_run,
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
    def test_pipeline_run_skipped_triggered(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_SKIPPED_TRIGGERED,
                       instance=self.pipeline_run,
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
    def test_pipeline_run_skipped(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_SKIPPED,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_resumed(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_RESUMED,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_restarted(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_RESTARTED,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_resumed_triggered(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_RESUMED_TRIGGERED,
                       instance=self.pipeline_run,
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
    def test_pipeline_run_restarted_triggered(self,
                                              activitylogs_record,
                                              tracker_record,
                                              notifier_record,
                                              executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_RESTARTED_TRIGGERED,
                       instance=self.pipeline_run,
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
    def test_pipeline_run_new_status(self,
                                     activitylogs_record,
                                     tracker_record,
                                     notifier_record,
                                     executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_NEW_STATUS,
                       instance=self.pipeline_run,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_succeeded(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_SUCCEEDED,
                       instance=self.pipeline_run)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_failed(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_FAILED,
                       instance=self.pipeline_run)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_run_done(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=pipeline_run_events.PIPELINE_RUN_DONE,
                       instance=self.pipeline_run)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1


del AuditorBaseTest
