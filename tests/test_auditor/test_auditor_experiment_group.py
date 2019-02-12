# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import experiment_group as experiment_group_events
from factories.factory_experiment_groups import ExperimentGroupFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorExperimentGroupTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory()

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_created(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_CREATED,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_updated(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_UPDATED,
                       instance=self.experiment_group,
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
    def test_experiment_group_deleted(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_DELETED,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_viewed(self,
                                     activitylogs_record,
                                     tracker_record,
                                     notifier_record,
                                     executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_VIEWED,
                       instance=self.experiment_group,
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
    def test_experiment_group_archived(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_ARCHIVED,
                       instance=self.experiment_group,
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
    def test_experiment_group_restored(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_RESTORED,
                       instance=self.experiment_group,
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
    def test_experiment_group_bookmarked(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_BOOKMARKED,
                       instance=self.experiment_group,
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
    def test_experiment_group_unbookmarked(self,
                                           activitylogs_record,
                                           tracker_record,
                                           notifier_record,
                                           executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_UNBOOKMARKED,
                       instance=self.experiment_group,
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
    def test_experiment_group_stopped(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_STOPPED,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_resumed(self,
                                      activitylogs_record,
                                      tracker_record,
                                      notifier_record,
                                      executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_RESUMED,
                       instance=self.experiment_group,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_done(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_DONE,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 1
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_new_status(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_NEW_STATUS,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_experiments_viewed(self,
                                                 activitylogs_record,
                                                 tracker_record,
                                                 notifier_record,
                                                 executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_EXPERIMENTS_VIEWED,
                       instance=self.experiment_group,
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
    def test_experiment_group_iteration(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_ITERATION,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 1

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_random(self,
                                     activitylogs_record,
                                     tracker_record,
                                     notifier_record,
                                     executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_RANDOM,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_grid(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record,
                                   executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_GRID,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_hyperband(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_HYPERBAND,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_bo(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record,
                                 executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_BO,
                       instance=self.experiment_group)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_deleted_triggered(self,
                                                activitylogs_record,
                                                tracker_record,
                                                notifier_record,
                                                executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_DELETED_TRIGGERED,
                       instance=self.experiment_group,
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
    def test_experiment_group_stopped_triggered(self,
                                                activitylogs_record,
                                                tracker_record,
                                                notifier_record,
                                                executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_STOPPED_TRIGGERED,
                       instance=self.experiment_group,
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
    def test_experiment_group_resumed_triggered(self,
                                                activitylogs_record,
                                                tracker_record,
                                                notifier_record,
                                                executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_RESUMED_TRIGGERED,
                       instance=self.experiment_group,
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
    def test_experiment_group_statuses_viewed(self,
                                              activitylogs_record,
                                              tracker_record,
                                              notifier_record,
                                              executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_STATUSES_VIEWED,
                       instance=self.experiment_group,
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
    def test_experiment_group_metrics_viewed(self,
                                             activitylogs_record,
                                             tracker_record,
                                             notifier_record,
                                             executor_record):
        auditor.record(event_type=experiment_group_events.EXPERIMENT_GROUP_METRICS_VIEWED,
                       instance=self.experiment_group,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
