# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from events.registry import pipeline as pipeline_events
from factories.factory_pipelines import PipelineFactory
from tests.test_auditor.utils import AuditorBaseTest


@pytest.mark.auditor_mark
class AuditorPipelineTest(AuditorBaseTest):
    """Testing subscribed events"""
    EVENTS = pipeline_events.EVENTS

    def setUp(self):
        super().setUp()
        self.pipeline = PipelineFactory()
        self.tested_events = {
            pipeline_events.PIPELINE_CREATED,
            pipeline_events.PIPELINE_UPDATED,
            pipeline_events.PIPELINE_DELETED,
            pipeline_events.PIPELINE_CLEANED_TRIGGERED,
            pipeline_events.PIPELINE_VIEWED,
            pipeline_events.PIPELINE_ARCHIVED,
            pipeline_events.PIPELINE_RESTORED,
            pipeline_events.PIPELINE_BOOKMARKED,
            pipeline_events.PIPELINE_UNBOOKMARKED,
            pipeline_events.PIPELINE_DELETED_TRIGGERED,
        }

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_created(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_CREATED,
                       instance=self.pipeline)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_updated(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_UPDATED,
                       instance=self.pipeline,
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
    def test_pipeline_deleted(self,
                              activitylogs_record,
                              tracker_record,
                              notifier_record,
                              executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_DELETED,
                       instance=self.pipeline)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_cleaned_triggered(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_CLEANED_TRIGGERED,
                       instance=self.pipeline)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.executor_service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_pipeline_viewed(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record,
                             executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_VIEWED,
                       instance=self.pipeline,
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
    def test_pipeline_archived(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_ARCHIVED,
                       instance=self.pipeline,
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
    def test_pipeline_restored(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_RESTORED,
                       instance=self.pipeline,
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
    def test_pipeline_bookmarked(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_BOOKMARKED,
                       instance=self.pipeline,
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
    def test_pipeline_unbookmarked(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_UNBOOKMARKED,
                       instance=self.pipeline,
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
    def test_pipeline_triggered_deleted(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=pipeline_events.PIPELINE_DELETED_TRIGGERED,
                       instance=self.pipeline,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0


del AuditorBaseTest
