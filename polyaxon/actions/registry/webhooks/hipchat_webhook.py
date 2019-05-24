from typing import Dict

import conf

from actions.registry.webhooks.webhook import WebHookAction, WebHookActionExecutedEvent
from actions.utils import hipchat
from events.event import Event
from events.event_actions import EXECUTED
from options.registry.integrations import INTEGRATIONS_WEBHOOKS_HIPCHAT

HIPCHAT_WEBHOOK_ACTION_EXECUTED = 'hipchat_webhook_action.{}'.format(EXECUTED)


class HipChatWebHookActionExecutedEvent(WebHookActionExecutedEvent):
    event_type = HIPCHAT_WEBHOOK_ACTION_EXECUTED


class HipChatWebHookAction(WebHookAction):
    action_key = 'hipchat_webhook'
    name = 'HipChat WebHook'
    event_type = HIPCHAT_WEBHOOK_ACTION_EXECUTED
    description = "HipChat webhooks to send payload to a hipchat room."
    raise_empty_context = True

    @classmethod
    def _get_config(cls) -> Dict:
        """Configuration for hipchat webhooks.

        should be a list of urls and potentially a method.

        If no method is given, then by default we use POST.
        """
        return conf.get(INTEGRATIONS_WEBHOOKS_HIPCHAT)

    @classmethod
    def serialize_event_to_context(cls, event: Event) -> Dict:
        return hipchat.serialize_event_to_context(event)

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            'message': context.get('message'),
            'message_format': context.get('message_format', 'html'),
            'color': context.get('color'),
            'from': context.get('from', 'Polyaxon'),
            'attach_to': context.get('attach_to'),
            'notify': context.get('notify', False),
            'card': context.get('card')
        }
