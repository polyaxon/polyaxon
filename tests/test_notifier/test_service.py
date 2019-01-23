# pylint:disable=ungrouped-imports
from unittest.mock import patch

import pytest

import notifier

from action_manager.actions.email import EmailAction
from action_manager.actions.webhooks.discord_webhook import DiscordWebHookAction
from action_manager.actions.webhooks.hipchat_webhook import HipChatWebHookAction
from action_manager.actions.webhooks.mattermost_webhook import MattermostWebHookAction
from action_manager.actions.webhooks.pagerduty_webhook import PagerDutyWebHookAction
from action_manager.actions.webhooks.slack_webhook import SlackWebHookAction
from action_manager.actions.webhooks.webhook import WebHookAction
from db.models.notification import Notification, NotificationEvent
from event_manager.events.experiment import EXPERIMENT_SUCCEEDED, EXPERIMENT_VIEWED
from factories.factory_experiments import ExperimentFactory
from tests.utils import BaseTest


@pytest.mark.notifier_mark
class NotifierTest(BaseTest):
    DISABLE_AUDITOR = False

    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()

    @patch.object(EmailAction, 'execute')
    @patch.object(WebHookAction, 'execute')
    @patch.object(SlackWebHookAction, 'execute')
    @patch.object(MattermostWebHookAction, 'execute')
    @patch.object(PagerDutyWebHookAction, 'execute')
    @patch.object(HipChatWebHookAction, 'execute')
    @patch.object(DiscordWebHookAction, 'execute')
    def test_record_does_not_create_notification_for_non_tracked_events(self,
                                                                        discord_execute,
                                                                        hipchat_execute,
                                                                        pagerduty_execute,
                                                                        mattermost_execute,
                                                                        slack_execute,
                                                                        webhook_execute,
                                                                        email_execute):
        notification_events = NotificationEvent.objects.count()
        notifications = Notification.objects.count()

        notifier.record(event_type=EXPERIMENT_VIEWED,
                        instance=self.experiment)

        assert discord_execute.call_count == 0
        assert hipchat_execute.call_count == 0
        assert pagerduty_execute.call_count == 0
        assert mattermost_execute.call_count == 0
        assert slack_execute.call_count == 0
        assert webhook_execute.call_count == 0
        assert email_execute.call_count == 0

        assert NotificationEvent.objects.count() == notification_events
        assert Notification.objects.count() == notifications

    @patch.object(EmailAction, 'execute')
    @patch.object(WebHookAction, 'execute')
    @patch.object(SlackWebHookAction, 'execute')
    @patch.object(MattermostWebHookAction, 'execute')
    @patch.object(PagerDutyWebHookAction, 'execute')
    @patch.object(HipChatWebHookAction, 'execute')
    @patch.object(DiscordWebHookAction, 'execute')
    def test_record_creates_notification(self,
                                         discord_execute,
                                         hipchat_execute,
                                         pagerduty_execute,
                                         mattermost_execute,
                                         slack_execute,
                                         webhook_execute,
                                         email_execute):
        notification_events = NotificationEvent.objects.count()
        notifications = Notification.objects.count()

        notifier.record(event_type=EXPERIMENT_SUCCEEDED,
                        instance=self.experiment)

        assert discord_execute.call_count == 1
        assert hipchat_execute.call_count == 1
        assert pagerduty_execute.call_count == 1
        assert mattermost_execute.call_count == 1
        assert slack_execute.call_count == 1
        assert webhook_execute.call_count == 1
        assert email_execute.call_count == 1

        assert NotificationEvent.objects.count() == notification_events + 1
        assert Notification.objects.count() == notifications + 2
        notification_event = NotificationEvent.objects.last()
        notifications = Notification.objects.all()
        assert notification_event.event_type == EXPERIMENT_SUCCEEDED
        assert notification_event.content_object == self.experiment
        assert set(notifications.values_list('user__id', flat=True)) == {
            self.experiment.user.id, self.experiment.project.user.id}

    @patch.object(EmailAction, '_execute')
    @patch.object(WebHookAction, '_execute')
    @patch.object(SlackWebHookAction, '_execute')
    @patch.object(MattermostWebHookAction, '_execute')
    @patch.object(PagerDutyWebHookAction, '_execute')
    @patch.object(HipChatWebHookAction, '_execute')
    @patch.object(DiscordWebHookAction, '_execute')
    def test_record_execute_not_called_for_non_configured_actions(self,
                                                                  discord_execute,
                                                                  hipchat_execute,
                                                                  pagerduty_execute,
                                                                  mattermost_execute,
                                                                  slack_execute,
                                                                  webhook_execute,
                                                                  email_execute):
        notifier.record(event_type=EXPERIMENT_SUCCEEDED,
                        instance=self.experiment)

        assert discord_execute.call_count == 0
        assert hipchat_execute.call_count == 0
        assert pagerduty_execute.call_count == 0
        assert mattermost_execute.call_count == 0
        assert slack_execute.call_count == 0
        assert webhook_execute.call_count == 0
        assert email_execute.call_count == 1

        assert NotificationEvent.objects.count() == 1
        assert Notification.objects.count() == 2
        notification_event = NotificationEvent.objects.last()
        notifications = Notification.objects.all()
        assert notification_event.event_type == EXPERIMENT_SUCCEEDED
        assert notification_event.content_object == self.experiment
        assert set(notifications.values_list('user__id', flat=True)) == {
            self.experiment.user.id, self.experiment.project.user.id}
