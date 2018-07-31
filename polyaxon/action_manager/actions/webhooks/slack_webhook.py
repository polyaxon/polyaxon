from django.conf import settings

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from event_manager.event_actions import EXECUTED

SLACK_WEBHOOK_ACTION_EXECUTED = 'slack_webhook_action.{}'.format(EXECUTED)


class SlackWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = SLACK_WEBHOOK_ACTION_EXECUTED


class SlackWebHookAction(WebHookAction):
    action_key = 'slack_webhook'
    name = 'Slack WebHook'
    event_type = SLACK_WEBHOOK_ACTION_EXECUTED
    description = "Slack webhooks to send payload to Slack Incoming Webhooks."
    raise_empty_context = True

    @classmethod
    def _validate_config(cls, config):
        if not config:
            return []
        return cls._get_valid_config(config, 'channel')

    @classmethod
    def _get_config(cls):
        """Configuration for slack webhooks.

        should be a list of urls and potentially a method and channel.

        If no method is given, then by default we use POST.
        """
        return settings.INTEGRATIONS_SLACK_WEBHOOKS

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        return {
            'fallback': context.get('fallback'),
            'title': context.get('title'),
            'title_link': context.get('title_link'),
            'text': context.get('text'),
            'fields': context.get('fields'),
            'mrkdwn_in': ['text'],
            'footer_icon': context.get('footer_icon'),
            'footer': context.get('footer'),
            'color': context.get('color'),
        }

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get('channel')
        if channel:
            data['channel'] = channel

        return data
