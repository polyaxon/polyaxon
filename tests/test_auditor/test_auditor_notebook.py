# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import notebook as notebook_events
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorNotebookTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.notebook = NotebookJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorNotebookTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_started(self, activitylogs_record, tracker_record):
        auditor.record(event_type=notebook_events.NOTEBOOK_STARTED,
                       instance=self.notebook,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=notebook_events.NOTEBOOK_STOPPED,
                       instance=self.notebook,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_notebook_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=notebook_events.NOTEBOOK_VIEWED,
                       instance=self.notebook,
                       actor_id=1)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=notebook_events.NOTEBOOK_NEW_STATUS,
                       instance=self.notebook)

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
