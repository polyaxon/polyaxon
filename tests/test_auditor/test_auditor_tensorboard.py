# pylint:disable=ungrouped-imports

from unittest.mock import patch

from django.test import override_settings

import activitylogs
import auditor
import tracker

from event_manager.events import tensorboard as tensorboard_events
from factories.factory_plugins import TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class AuditorTensorboardTest(BaseTest):
    """Testing subscribed events"""

    def setUp(self):
        self.tensorboard = TensorboardJobFactory(project=ProjectFactory())
        auditor.validate()
        auditor.setup()
        tracker.validate()
        tracker.setup()
        activitylogs.validate()
        activitylogs.setup()
        super(AuditorTensorboardTest, self).setUp()

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_tensorboard_started(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_STARTED,
                       instance=self.tensorboard,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_tensorboard_started_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_STARTED_TRIGGERED,
                       instance=self.tensorboard,
                       actor_id=1,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_tensorboard_stopped(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_STOPPED,
                       instance=self.tensorboard,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_tensorboard_stopped_triggered(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_STOPPED_TRIGGERED,
                       instance=self.tensorboard,
                       actor_id=1,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_tensorboard_viewed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_VIEWED,
                       instance=self.tensorboard,
                       actor_id=1,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 1

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_new_status(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_NEW_STATUS,
                       instance=self.tensorboard,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_failed(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_FAILED,
                       instance=self.tensorboard,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0

    @patch('tracker.service.TrackerService.record_event')
    @patch('activitylogs.service.ActivityLogService.record_event')
    def test_experiment_succeeded(self, activitylogs_record, tracker_record):
        auditor.record(event_type=tensorboard_events.TENSORBOARD_SUCCEEDED,
                       instance=self.tensorboard,
                       target='project')

        assert tracker_record.call_count == 1
        assert activitylogs_record.call_count == 0
