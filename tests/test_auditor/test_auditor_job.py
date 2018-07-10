# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import activitylogs
import auditor
import tracker

from event_manager.events import job as job_events
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorJobTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.job = NotebookJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super().setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_created(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_CREATED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_updated(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_UPDATED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_started(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_STARTED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_started_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_STARTED_TRIGGERED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_DELETED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_triggered_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_DELETED_TRIGGERED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_STOPPED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_stopped_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_STOPPED_TRIGGERED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_VIEWED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_bookmarked(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_BOOKMARKED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_NEW_STATUS,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_failed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_FAILED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_succeeded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_SUCCEEDED,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_done(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_DONE,
                       instance=self.job)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_logs_viewed_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_LOGS_VIEWED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_restarted_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_RESTARTED_TRIGGERED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_statuses_viewed_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_outputs_downloaded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=job_events.JOB_OUTPUTS_DOWNLOADED,
                       instance=self.job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
