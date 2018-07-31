# pylint:disable=ungrouped-imports
import pytest

import notifier

from db.models.notification import Notification, NotificationEvent
from event_manager.events.experiment import EXPERIMENT_SUCCEEDED
from factories.factory_experiments import ExperimentFactory
from tests.utils import BaseTest


@pytest.mark.notifier_mark
class NotifierTest(BaseTest):
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        notifier.validate()
        notifier.setup()

    def test_record_creates_notification(self):
        notifier.record(event_type=EXPERIMENT_SUCCEEDED,
                        instance=self.experiment)

        assert NotificationEvent.objects.count() == 1
        assert Notification.objects.count() == 2
        notification_event = NotificationEvent.objects.last()
        notifications = Notification.objects.all()
        assert notification_event.event_type == EXPERIMENT_SUCCEEDED
        assert notification_event.content_object == self.experiment
        assert set(notifications.values_list('user__id', flat=True)) == {
            self.experiment.user.id, self.experiment.project.user.id}
