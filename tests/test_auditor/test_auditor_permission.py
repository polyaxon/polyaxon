# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from event_manager.events import permission as permission_events
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorPermissionTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_project_denied(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=permission_events.PERMISSION_PROJECT_DENIED,
                       id=1,
                       user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_repo_denied(self,
                                    activitylogs_record,
                                    tracker_record,
                                    notifier_record,
                                    executor_record):
        auditor.record(event_type=permission_events.PERMISSION_REPO_DENIED,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_group_denied(self,
                                                activitylogs_record,
                                                tracker_record,
                                                notifier_record,
                                                executor_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_GROUP_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_denied(self,
                                          activitylogs_record,
                                          tracker_record,
                                          notifier_record,
                                          executor_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_tensorboard_denied(self,
                                           activitylogs_record,
                                           tracker_record,
                                           notifier_record,
                                           executor_record):
        auditor.record(event_type=permission_events.PERMISSION_TENSORBOARD_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_notebook_denied(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record,
                                        executor_record):
        auditor.record(event_type=permission_events.PERMISSION_NOTEBOOK_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_build_job_denied(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=permission_events.PERMISSION_BUILD_JOB_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_job_denied(self,
                                              activitylogs_record,
                                              tracker_record,
                                              notifier_record,
                                              executor_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_JOB_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_cluster_denied(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        auditor.record(event_type=permission_events.PERMISSION_CLUSTER_DENIED,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_user_role_denied(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record,
                                         executor_record):
        auditor.record(event_type=permission_events.PERMISSION_USER_ROLE_DENIED,
                       user_id=2,
                       actor_id=1,
                       actor_name='foo',
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
