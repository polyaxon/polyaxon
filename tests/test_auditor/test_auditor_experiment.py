# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import experiment as experiment_events
from factories.factory_experiments import ExperimentFactory, ExperimentMetricFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorExperimentTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_created(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_CREATED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_updated(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_UPDATED,
                       instance=self.experiment,
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
    def test_experiment_deleted(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_DELETED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_cleaned_triggered(self,
                                          activitylogs_record,
                                          tracker_record,
                                          notifier_record,
                                          executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_CLEANED_TRIGGERED,
                       instance=self.experiment)

        assert tracker_record.call_count == 0
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_viewed(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_archived(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_ARCHIVED,
                       instance=self.experiment,
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
    def test_experiment_restored(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESTORED,
                       instance=self.experiment,
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
    def test_experiment_bookmarked(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_BOOKMARKED,
                       instance=self.experiment,
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
    def test_experiment_unbookmarked(self,
                                     activitylogs_record,
                                     tracker_record,
                                     notifier_record,
                                     executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_UNBOOKMARKED,
                       instance=self.experiment,
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
    def test_experiment_stopped(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STOPPED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_resumed(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESUMED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_restarted(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESTARTED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_copied(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_COPIED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_status(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_NEW_STATUS,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_metric(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_NEW_METRIC,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

        # Adding a metric will trigger a record creation automatically
        ExperimentMetricFactory(experiment=self.experiment)

        assert tracker_record.call_count == 2
        assert activitylogs_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_succeeded(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_SUCCEEDED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_failed(self,
                               activitylogs_record,
                               tracker_record,
                               notifier_record,
                               executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_FAILED,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_done(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record,
                             executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_DONE,
                       instance=self.experiment)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_resources_viewed(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESOURCES_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_logs_viewed(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_LOGS_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_outputs_downloaded(self,
                                           activitylogs_record,
                                           tracker_record,
                                           notifier_record,
                                           executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_OUTPUTS_DOWNLOADED,
                       instance=self.experiment,
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
    def test_experiment_statuses_viewed(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STATUSES_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_jobs_viewed(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_JOBS_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_metrics_viewed(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_METRICS_VIEWED,
                       instance=self.experiment,
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
    def test_experiment_triggered_deleted(self,
                                          activitylogs_record,
                                          tracker_record,
                                          notifier_record,
                                          executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_DELETED_TRIGGERED,
                       instance=self.experiment,
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
    def test_experiment_triggered_stopped(self,
                                          activitylogs_record,
                                          tracker_record,
                                          notifier_record,
                                          executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_STOPPED_TRIGGERED,
                       instance=self.experiment,
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
    def test_experiment_triggered_resumed(self,
                                          activitylogs_record,
                                          tracker_record,
                                          notifier_record,
                                          executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESUMED_TRIGGERED,
                       instance=self.experiment,
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
    def test_experiment_triggered_restarted(self,
                                            activitylogs_record,
                                            tracker_record,
                                            notifier_record,
                                            executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_RESTARTED_TRIGGERED,
                       instance=self.experiment,
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
    def test_experiment_triggered_copied(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=experiment_events.EXPERIMENT_COPIED_TRIGGERED,
                       instance=self.experiment,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
