# pylint:disable=ungrouped-imports

from unittest.mock import patch

import pytest

import activitylogs
import auditor
import tracker

from constants import content_types
from db.models.searches import Search
from event_manager.events import search as searches_events
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.auditor_mark
class AuditorSearchesTest(BaseTest):
    """Testing subscribed events"""
    DISABLE_RUNNER = False

    def setUp(self):
        self.project = ProjectFactory()
        self.user = self.project.user
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super().setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_search_created(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.BUILD_JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_search_created(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_search_created(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_search_created(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT_GROUP,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_CREATED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_build_search_deleted(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.BUILD_JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_job_search_deleted(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.JOB,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_search_deleted(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_group_search_deleted(self, activitylogs_record, tracker_record):
        search = Search.objects.create(project=self.project,
                                       content_type=content_types.EXPERIMENT_GROUP,
                                       user=self.user,
                                       query={})
        auditor.record(event_type=searches_events.SEARCH_DELETED,
                       instance=search)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1
