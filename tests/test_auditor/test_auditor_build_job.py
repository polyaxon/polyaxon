# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import activitylogs
import auditor
import tracker

from event_manager.events import build_job as build_job_events
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorBuildJobTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.build_job = BuildJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorBuildJobTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_created(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_CREATED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_updated(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_UPDATED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_started(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_started_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED_TRIGGERED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_DELETED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_triggered_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_DELETED_TRIGGERED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_stopped_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED_TRIGGERED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_VIEWED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_NEW_STATUS,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_failed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_FAILED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_succeeded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_SUCCEEDED,
                       instance=self.build_job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_logs_viewed_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_LOGS_VIEWED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_job_statuses_viewed_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STATUSES_VIEWED,
                       instance=self.build_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
