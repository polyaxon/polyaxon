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
        self.notebook = BuildJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorBuildJobTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_started(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED,
                       instance=self.notebook,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_started_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STARTED_TRIGGERED,
                       instance=self.notebook,
                       target='project',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED,
                       instance=self.notebook,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_stopped_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_STOPPED_TRIGGERED,
                       instance=self.notebook,
                       target='project',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_VIEWED,
                       instance=self.notebook,
                       target='project',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_NEW_STATUS,
                       instance=self.notebook,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_failed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_FAILED,
                       instance=self.notebook,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_succeeded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=build_job_events.BUILD_JOB_SUCCEEDED,
                       instance=self.notebook,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
