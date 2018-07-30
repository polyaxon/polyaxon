from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from event_manager.event_actions import EXECUTED

SLACK_WEBHOOK_ACTION_EXECUTED = 'slack_webhook_action.{}'.format(EXECUTED)


class SlackWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = SLACK_WEBHOOK_ACTION_EXECUTED


class SlackWebHookAction(WebHookAction):
    key = 'slack_webhook'
    name = 'Slack WebHook'
    event_type = SLACK_WEBHOOK_ACTION_EXECUTED
    description = "Slack webhooks to send payload to Slack Incoming Webhooks."

    def _get_config(self):
        """Configuration for slack webhooks.

        should be a list of urls and potentially a method and channel.

        If no method is given, then by default we use POST.
        """
        return self._get_from_settings(settings.INTEGRATIONS_SLACK_WEBHOOKS, 'channel')

    def _prepare(self, context):
        # Add slack specific handling
        return context

    def _pre_execute_web_hook(self, data, config):
        channel = config.get('channel')
        if channel:
            data['channel'] = channel

        return data
