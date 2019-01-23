# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import auditor

from constants import content_types
from db.models.searches import Search
from event_manager.events import search as searches_events
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorSearchesTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_AUDITOR = False
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.user = self.project.user

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_search_created(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.BUILD_JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_search_created(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_search_created(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_search_created(self,
                                             activitylogs_record,
                                             tracker_record,
                                             notifier_record,
                                             executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT_GROUP,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_search_deleted(self,
                                  activitylogs_record,
                                  tracker_record,
                                  notifier_record,
                                  executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.BUILD_JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_search_deleted(self,
                                activitylogs_record,
                                tracker_record,
                                notifier_record,
                                executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_search_deleted(self,
                                       activitylogs_record,
                                       tracker_record,
                                       notifier_record,
                                       executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0

    @patch('executor.service.ExecutorService.record_event')
    @patch('notifier.service.NotifierService.record_event')
    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_search_deleted(self,
                                             activitylogs_record,
                                             tracker_record,
                                             notifier_record,
                                             executor_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT_GROUP,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
        assert notifier_record.call_count == 0
        assert executor_record.call_count == 0
