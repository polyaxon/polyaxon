from typing import Dict

import conf

from action_manager.actions.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from action_manager.utils import slack
from event_manager.event import Event
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
        return cls._get_valid_config(config, 'channel', 'icon_url')

    @classmethod
    def _get_config(cls):
        """Configuration for slack webhooks.

        should be a list of urls and potentially a method and channel.

        If no method is given, then by default we use POST.
        """
        return conf.get('INTEGRATIONS_SLACK_WEBHOOKS')

    @classmethod
    def serialize_event_to_context(cls, event: Event) -> Dict:
        return slack.serialize_event_to_context(event)

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        data = {
            'fallback': context.get('fallback'),
            'title': context.get('title'),
            'title_link': context.get('title_link'),
            'text': context.get('text'),
            'fields': context.get('fields'),
            'mrkdwn_in': context.get('mrkdwn_in'),
            'footer_icon': context.get('footer_icon'),
            'footer': context.get('footer', 'Polyaxon'),
            'color': context.get('color'),
        }
        return {'attachments': [data]}

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get('channel')
        icon_url = config.get('channel')
        if channel:
            data['channel'] = channel

        if icon_url:
            data['icon_url'] = icon_url

        return data
