# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import permission as permission_events
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorPermissionTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.notebook = NotebookJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorPermissionTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_project_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_PROJECT_DENIED,
                       id=1,
                       user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_repo_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_REPO_DENIED,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_group_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_GROUP_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_tensorboard_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_TENSORBOARD_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_notebook_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_NOTEBOOK_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_experiment_job_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_EXPERIMENT_JOB_DENIED,
                       id=1,
                       user_id=2,
                       project_id=1,
                       project_user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_cluster_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_CLUSTER_DENIED,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_permission_user_role_denied(self, activitylogs_record, tracker_record):
        auditor.record(event_type=permission_events.PERMISSION_USER_ROLE_DENIED,
                       user_id=2,
                       actor_id=1,
                       event='some.event')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
