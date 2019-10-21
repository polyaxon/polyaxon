import uuid

from datetime import timedelta

import pytest

import conf

from crons.tasks.cleaning import clean_activity_logs, clean_notifications
from db.models.activitylogs import ActivityLog
from db.models.notification import Notification, NotificationEvent
from events.registry.experiment import EXPERIMENT_SUCCEEDED
from factories.factory_experiments import ExperimentFactory
from factories.factory_users import UserFactory
from options.registry.cleaning import (
    CLEANING_INTERVALS_ACTIVITY_LOGS,
    CLEANING_INTERVALS_NOTIFICATIONS
)
from tests.base.case import BaseTest


@pytest.mark.crons_mark
class TestCleaningCrons(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()
        self.user = UserFactory()

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_clean_activity_logs(self):
        actvity_logs_count = ActivityLog.objects.count()
        notification_events_counts = NotificationEvent.objects.count()
        notifications_counts = Notification.objects.count()

        ActivityLog.objects.create(
            event_type=EXPERIMENT_SUCCEEDED,
            actor_id=self.user.id,
            context={},
            created_at=self.experiment.created_at,
            content_object=self.experiment,
            ref=uuid.uuid4()
        )
        ActivityLog.objects.create(
            event_type=EXPERIMENT_SUCCEEDED,
            actor_id=self.user.id,
            context={},
            created_at=self.experiment.created_at - timedelta(
                days=conf.get(CLEANING_INTERVALS_ACTIVITY_LOGS) + 3),
            content_object=self.experiment,
            ref=uuid.uuid4()
        )

        notification_event = NotificationEvent.objects.create(
            event_type=EXPERIMENT_SUCCEEDED,
            actor_id=self.user.id,
            context={},
            created_at=self.experiment.created_at,
            content_object=self.experiment
        )
        Notification.objects.create(
            user=self.user,
            event=notification_event
        )
        notification_event = NotificationEvent.objects.create(
            event_type=EXPERIMENT_SUCCEEDED,
            actor_id=self.user.id,
            context={},
            created_at=self.experiment.created_at - timedelta(
                days=conf.get(CLEANING_INTERVALS_NOTIFICATIONS) + 3),
            content_object=self.experiment
        )
        Notification.objects.create(
            user=self.user,
            event=notification_event
        )
        assert ActivityLog.objects.count() == actvity_logs_count + 2
        assert NotificationEvent.objects.count() == notification_events_counts + 2
        assert Notification.objects.count() == notifications_counts + 2

        clean_activity_logs()

        assert ActivityLog.objects.count() == actvity_logs_count + 1
        assert NotificationEvent.objects.count() == notification_events_counts + 2
        assert Notification.objects.count() == notifications_counts + 2

        clean_notifications()

        assert ActivityLog.objects.count() == actvity_logs_count + 1
        assert NotificationEvent.objects.count() == notification_events_counts + 1
        assert Notification.objects.count() == notifications_counts + 1
