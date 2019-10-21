from typing import Dict, List

import conf

from actions.registry.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from actions.utils import mattermost
from events.event import Event
from events.event_actions import EXECUTED
from options.registry.integrations import INTEGRATIONS_WEBHOOKS_MATTERMOST

MATTERMOST_WEBHOOK_ACTION_EXECUTED = 'mattermost_webhook_action.{}'.format(EXECUTED)


class MattermostWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = MATTERMOST_WEBHOOK_ACTION_EXECUTED


class MattermostWebHookAction(WebHookAction):
    action_key = 'mattermost_webhook'
    name = 'Mattermost WebHook'
    event_type = MATTERMOST_WEBHOOK_ACTION_EXECUTED
    description = "Mattermost webhooks to send payload to a Mattermost channel."
    raise_empty_context = True

    @classmethod
    def _validate_config(cls, config: Dict) -> List[Dict]:
        if not config:
            return []
        return cls._get_valid_config(config, 'channel')

    @classmethod
    def _get_config(cls) -> List[Dict]:
        """Configuration for mattermost webhooks.

        should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return conf.get(INTEGRATIONS_WEBHOOKS_MATTERMOST)

    @classmethod
    def serialize_event_to_context(cls, event: Event) -> Dict:
        return mattermost.serialize_event_to_context(event)

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        data = {
            'pretext': context.get('pretext'),
            'title': context.get('title'),
            'text': context.get('text'),
            'color': context.get('color'),
            'fields': context.get('fields'),
            'author_name': context.get('author_name', 'Polyaxon'),
            'author_link': context.get('author_link', 'https://polyaxon.com'),
            'author_icon': context.get('author_icon')
        }
        return {'attachments': [data]}

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get('channel')
        if channel:
            data['channel'] = channel

        return data
