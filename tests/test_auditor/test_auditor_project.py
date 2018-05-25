# pylint:disable=ungrouped-imports

from unittest.mock import patch

import activitylogs
import auditor
import tracker

from event_manager.events import project as project_events
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


class AuditorProjectTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.project = ProjectFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorProjectTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_created(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_CREATED,
                       instance=self.project)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_updated(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_UPDATED,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_deleted(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_DELETED,
                       instance=self.project)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_deleted_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_DELETED_TRIGGERED,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_VIEWED,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_set_public(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_SET_PUBLIC,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_set_private(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_SET_PRIVATE,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_experiment_groups_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_EXPERIMENT_GROUPS_VIEWED,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_experiment_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=project_events.PROJECT_EXPERIMENTS_VIEWED,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
