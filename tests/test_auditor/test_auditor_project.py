# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import activitylogs
import auditor
import notifier
import tracker

from event_manager.events import project as project_events
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorProjectTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_RUNNER = True

    def setUp(self):
        self.project = ProjectFactory()
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        notifier.validate()
        notifier.setup()
        super().setUp()

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_created(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record):
        auditor.record(event_type=project_events.PROJECT_CREATED,
                       instance=self.project)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_updated(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record):
        auditor.record(event_type=project_events.PROJECT_UPDATED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_deleted(self,
                             activitylogs_record,
                             tracker_record,
                             notifier_record):
        auditor.record(event_type=project_events.PROJECT_DELETED,
                       instance=self.project)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_deleted_triggered(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record):
        auditor.record(event_type=project_events.PROJECT_DELETED_TRIGGERED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_viewed(self,
                            activitylogs_record,
                            tracker_record,
                            notifier_record):
        auditor.record(event_type=project_events.PROJECT_VIEWED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_unbookmarked(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record):
        auditor.record(event_type=project_events.PROJECT_UNBOOKMARKED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_bookmarked(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record):
        auditor.record(event_type=project_events.PROJECT_BOOKMARKED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_set_public(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record):
        auditor.record(event_type=project_events.PROJECT_SET_PUBLIC,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_set_private(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record):
        auditor.record(event_type=project_events.PROJECT_SET_PRIVATE,
                       instance=self.project,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_experiment_groups_viewed(self,
                                              activitylogs_record,
                                              tracker_record,
                                              notifier_record):
        auditor.record(event_type=project_events.PROJECT_EXPERIMENT_GROUPS_VIEWED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_experiments_viewed(self,
                                        activitylogs_record,
                                        tracker_record,
                                        notifier_record):
        auditor.record(event_type=project_events.PROJECT_EXPERIMENTS_VIEWED,
                       instance=self.project,
                       actor_name='foo',
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_jobs_viewed(self,
                                 activitylogs_record,
                                 tracker_record,
                                 notifier_record):
        auditor.record(event_type=project_events.PROJECT_JOBS_VIEWED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_builds_viewed(self,
                                   activitylogs_record,
                                   tracker_record,
                                   notifier_record):
        auditor.record(event_type=project_events.PROJECT_BUILDS_VIEWED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0

    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_project_tensorboards_viewed(self,
                                         activitylogs_record,
                                         tracker_record,
                                         notifier_record):
        auditor.record(event_type=project_events.PROJECT_TENSORBOARDS_VIEWED,
                       instance=self.project,
                       actor_id=1,
                       actor_name='foo')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
