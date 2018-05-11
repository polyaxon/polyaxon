# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import experiment as experiment_events
from factories.factory_experiments import ExperimentFactory, ExperimentMetricFactory
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorExperimentTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.experiment = ExperimentFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorExperimentTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_created(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_CREATED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_updated(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_UPDATED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_DELETED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STOPPED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_resumed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESUMED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_restarted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESTARTED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_copied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_COPIED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_NEW_STATUS,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_metric(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_NEW_METRIC,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

        # Adding a metric will trigger a record creation automatically
        ExperimentMetricFactory(experiment=self.experiment)

        assert tracker_record.call_count == 2
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_succeeded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_SUCCEEDED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_failed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_FAILED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_resources_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESOURCES_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_logs_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_LOGS_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_statuses_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STATUSES_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_jobs_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_JOBS_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_metrics_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_METRICS_VIEWED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_triggered_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_DELETED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_triggered_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STOPPED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_triggered_resumed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESUMED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_triggered_restarted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESTARTED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_triggered_copied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_COPIED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
