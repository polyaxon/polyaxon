# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import experiment_job as experiment_job_events
from factories.factory_experiments import ExperimentJobFactory
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorExperimentJobTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.experiment_job = ExperimentJobFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorExperimentJobTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_job_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_job_events.EXPERIMENT_JOB_VIEWED,
                       instance=self.experiment_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_resources_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_job_events.EXPERIMENT_JOB_RESOURCES_VIEWED,
                       instance=self.experiment_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_logs_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_job_events.EXPERIMENT_JOB_LOGS_VIEWED,
                       instance=self.experiment_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_statuses_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_job_events.EXPERIMENT_JOB_STATUSES_VIEWED,
                       instance=self.experiment_job,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
